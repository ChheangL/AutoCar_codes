import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from pylab import *
from scipy.ndimage import filters
import pandas as pd
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
                self.lines_frame = self.cvs_to_object()
                print('load CVS file successfully')
            except:
                print('Calculating Frame ...')
                self.lines_frame = self.get_frame_coordinate(width=self.width,hight=self.height,theta=self.angle)
                self.convert_to_cvs()
                print('Done!')
            
    def plot_some_line(self,string):
        plt.axis([0.0,self.width,0.0,self.height])
        plt.plot(self.lines_frame[:,0],self.lines_frame[:,1],string)

    def plot_all_line(self,string):
        plt.axis([0.0,self.width,0.,self.height])
        for key in self.lines_frame.keys():
            plt.plot(self.lines_frame[key][:,0],self.lines_frame[key][:,1],string)
            
    def get_data(self,img_path,D):
        img = np.array(Image.open(img_path).convert('L'))
        #img = 255.0*(img/255.0)**6
        img = filters.gaussian_filter(img,D)
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
    def convert_to_cvs(self):
        data_frame = pd.DataFrame([self.lines_frame])
        data_frame.to_csv((str(self.width)+'x'+str(self.height)+'_'+str(self.angle)+'frame.cvs'),index=False)
    
    def cvs_to_object(self):
        data_frame = pd.read_csv((str(self.width)+'x'+str(self.height)+'_'+str(self.angle)+'frame.cvs'))
        data = {}
        for key in data_frame:
            data[key] = data_frame[key][0].replace('[','').replace(']','').replace('  ',' ').replace('   ',' ').split('\n')
            array = np.empty((0,2),float)
            for item in data[key]:
                values=item.split(' ')
                if values[-2] != '' and  values[-1]!= '':
                    array = np.append(array,[[float(values[-2]), float(values[-1])]],axis=0)
                data[key] = array
        return data