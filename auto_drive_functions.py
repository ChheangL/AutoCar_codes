import numpy as np
import math
import matplotlib.pyplot as plt
from ImageFrame import Frame
from pylab import *
from EdgeFinder import EdgeFinder as ef
from PIL import Image


def mid_angle(data,width,height):
    total_point = int(len(data))
    data_per_side = int(total_point/2)
    values = np.empty((0,3),float)
    for i in range (0, data_per_side):
        if np.isnan(data[i][0]) or np.isnan(data[-(i+1)][0]):
            continue
        else:
            mid = (data[i] + data[-(i+1)])/2
            if mid[0]-(width/2.) != 0.0:
                tan = (mid[1]-height)/(mid[0]-(width/2.))
                angle_radiant = math.atan(tan)
                angle_degree = math.degrees(angle_radiant)
                #print(angle_degree)
                angle = ((-1)*angle_degree if angle_degree < 0 else 180-angle_degree)
            else :
                angle = 90.0
            values = np.append(values,[np.append(mid,[angle])],axis=0)
    return values

def perform_3sig(data,s1,hd,plot=True):
    edges = {}
    for key in data.keys():
        detect = ef(s1,hd,data[key][:,2])
        if plot : detect.plot_data(lines = key)
        if 'num' in detect.abnormal.keys():
            index_edg = detect.abnormal['num']
            edges[key] = data[key][index_edg]
        else:
            edges[key]= [np.NaN,np.NaN,np.NaN]
    return edges

def plot_on_img(img,edges,frame,mid_points=np.array([])):
    img = np.array(img)
    height,width = img.shape
    plt.axis([0.0,width,0.0,height])
    gray()
    imshow(img)
    if mid_points.size != 0: plt.plot(mid_points[:,0],mid_points[:,1],'bo')
    frame.plot_all_line('k')
    for key in edges.keys():
        #print(edges[key][0])
        plt.plot(edges[key][0],edges[key][1],'ro')
    plt.show

def retrieve_angle(s1,hd,img_path,frame,plot = False):
    data = frame.get_data(img_path,1)
    edges = perform_3sig(data,s1,hd,False)
    points = np.empty((0,2),float)
    for key in edges.keys():
        points = np.append(points,[edges[key][0:2]],axis=0)
    #print(mids_point[:,2])
    mid_points = mid_angle(points,frame.width,frame.height)
    if plot : plot_on_img(img_path,edges,frame,mid_points)
    return mid_points[:,2]