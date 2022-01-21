import numpy as np
import pandas as pd
import pickle as pk
class Frame:
    """get the coordinate to the lines based on the angle, width and hight provided
    """
    
        
    def get_frame_coordinate(self,width,hight,theta):
        lines_frame = {} #creating empty dictionary
        for line in range(1,int(180/theta)):    
            lines_frame['L'+str(line)] = np.empty((0,2),float)#np.array([[0.,0.]])
        angle = np.radians(theta)
        c, s = np.cos(angle), np.sin(angle)
        R = np.array(((c, -s), (s, c))) # the rotating matrix (x -> x')
        #building a i by j matrix 
        for i in range(0,int(hight)):
            for j in range(0,int(width)):
                current = np.array([j-width/2.0,i-hight]) #the translating origin ( x -> -width/2 , y -> -hight)
                rotated = current
                for line in range(1,int(180/theta)):    
                    rotated = np.matmul(R,rotated) #rotate (x -> x')
                    #check for pixel around that line
                    if rotated[1]<0.2 and rotated[1]>-0.2:
                        B = np.array(((c, s), (-s, c))) #the rotating matrix  (x' -> x)
                        for num in range(0,line):
                            rotated = np.matmul(B,rotated) #rotate back (x' -> x)
                        rotated = np.around(rotated+[width/2.0,hight]) #the translating back origin again ( x -> width/2 , y -> hight)
                        #append to dictionary
                        if rotated[0]<width and rotated[1]<hight:
                            if (lines_frame['L'+str(line)].size==0)or(rotated[1]!=lines_frame['L'+str(line)][-1][1]):
                                lines_frame['L'+str(line)] = np.append(lines_frame['L'+str(line)],[rotated],axis=0)
            print('*',end='')
        return lines_frame
    def __init__(self, width, height, angle):
            self.width = width
            self.height = height
            self.angle = angle
            try:
                self.lines_frame = self.unserilize().lines_frame
            except:
                print('Calculating Frame ...')
                self.lines_frame = self.get_frame_coordinate(width=self.width,hight=self.height,theta=self.angle)
                self.serilization()
                print('Done!')
            
   
    def get_data(self,img,D):
        img = np.array(img)
        #img = 255.0*(img/255.0)**6
        #self.plot_all_line('k')
        #imshow(img)
        lines = {}
        for key in self.lines_frame.keys():
            count = 0
            temp2 = np.empty((0,3),float)
            for cord in self.lines_frame[key]:
                #print(lines[key][count])
                temp1 = np.append(self.lines_frame[key][count], [img[int(cord[1]),int(cord[0])]])
                temp2 = np.append(temp2,[temp1],axis=0)
                count+=1
            lines[key] = np.flip(temp2,axis=0)
        return lines
    #save lines_frame to cvs as 'frame.cvs'

    def serilization(self):
        with open((str(self.width)+'x'+str(self.height)+'_'+str(self.angle)+'frame.pkl'), 'wb') as f:
            pk.dump(self, f)
            
    def unserilize(self):
        with open((str(self.width)+'x'+str(self.height)+'_'+str(self.angle)+'frame.pkl'), 'rb') as f:
            print('load CVS file successfully')
            return pk.load(f)
        
        