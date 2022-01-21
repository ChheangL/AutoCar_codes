from auto_drive_functions import retrieve_angle
from ImageFrame import Frame
import cv2

frame1 = Frame(1280,720,10)
cam = cv2.VideoCapture(0)


def main():
    img = cv2.cvtColor(cam.read()[1],cv2.COLOR_BGR2GRAY)
    angle = retrieve_angle(s1= 60,hd=5,img = img,frame = frame1,plot=True)
    print(angle)
    
main()