import numpy as np
import matplotlib.pyplot as plt

class EdgeFinder :
    """
       This perform the 3-sigma method on a single dimension data set
       Attribue : 
           data (numpy array)
           s1 (int)
           hd (int)
           abnormal (dictionary)
       Method :
           return(void)       __init__(self,s1,hd,data) : is a constructor
           return(list)       get_3sigmaBound(self,data_seg) : for getting the boundary in the interval
           return(dictionary) check_abnormal(self,init) : perform checking for the hd interval
           return(dictionary) perform_3sig(self) : perform the 3 sigma method for the entier data set
           return(void)       plot_data(self) : ploting the data on the gra
    """
    def __init__(self,s1,hd,Data):
        self.data = Data
        self.s1 = s1
        self.hd = hd
        self.perform_3sig()
        
    #get the upper and lower bound
    def get_3sigmaBound(self,data):
        mean = np.mean(data)
        standard_div = np.std(data)
        upperbound = mean + 3*standard_div
        lowerbound = mean - 3*standard_div
        return [upperbound, lowerbound]
    
    #the function that do the stuff above
    def check_abnormal(self,init):
        states={} #empty dictionary discribing the current interveral data
        end=init+self.s1 #a stop for the s1 interval
        states['num'] = end #start checking at that posision of data

        #get the upperbound and lowerbound of the data
        states['up'],states['low'] = self.get_3sigmaBound(self.data[init : end])

        #loop and check for abnormal data with upper and lower bound
        for Data in self.data[end:end+self.hd]:
            #if found abnormal, return the dictionary
            if Data >= states['up'] or Data <= states['low']: return states
            states['num'] += 1
        #loop is done, and num is noted at Nan
        states['num'] = np.NaN
        return states

    def perform_3sig(self):
        init = 0 #act as the starting position for the operation
        result = {'up':[],'low':[]} #empty dictionary for result appending
        while True:
            #limter for operation going over the data value
            if init+self.s1+self.hd >= len(self.data) : break
            #call in the operation to check the abnormal value
            states = self.check_abnormal(init)
            result['low'].append(states['low']) # append everything to the result
            result['up'].append(states['up'])
            #check if the data found a abnormal. if so, the operation terminate
            if not np.isnan(states['num']) :
                result['num'] = states['num']
                break
            #move to next hd
            init += self.hd 
        self.abnormal = result
        return result
     
    def plot_data(self):
        plt.plot(self.data,'r')
        for interation in range(0,len(self.abnormal['low'])):
            i1 = interation*(self.hd)  
            e1 = self.s1+self.hd*interation
            i2 = e1
            e2 = self.s1+self.hd*interation+self.hd
            plt.plot(range(i1,e1),np.full(shape=self.s1,fill_value = self.abnormal['low'][interation]),'m',)
            plt.plot(range(i2,e2),np.full(shape=self.hd,fill_value = self.abnormal['low'][interation]),'k',)
            plt.plot(range(i1,e1),np.full(shape=self.s1,fill_value = self.abnormal['up'][interation]),'m')
            plt.plot(range(i2,e2),np.full(shape=self.hd,fill_value = self.abnormal['up'][interation]),'k')
        if 'num' in self.abnormal.keys() : plt.plot([self.abnormal['num']],self.data[self.abnormal['num']],'bo',)
        plt.show()