import cv2
import numpy as np
from Graficos import *
from Robot import *
from ClassServer import *

def camara(Server):
    img=cv2.VideoCapture(0)
    Server.camara=True
        
    while True:
        _, frame = img.read()
        for r in Server.listaR:
            
            hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            th1=cv2.inRange(hsv,r.HSV_MIN,r.HSV_MAX)
            th1=Morpho(th1)
                
            seguimiento_robots(r,th1,hsv,frame)
            
        cv2.imshow("Camara 1",frame)
        cv2.imshow("threshold cam 1",th1)
        cv2.waitKey(1)

def Morpho(th1):
    kernel1=np.ones((3,3),np.uint8)
    kernel2=np.ones((4,4),np.uint8)
    th1=cv2.erode(th1,kernel1,iterations=1)
    th1=cv2.dilate(th1,kernel2,iterations=1)
    return th1

def seguimiento_robots(r,th1,hsv,frame):
    MIN_AREA=20*20
    MAX_AREA=150*150
    temp=th1.copy()
    contorno,hierarchy=cv2.findContours(temp,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
    
    if hierarchy==None:
        hierarchy=np.array([[[]]])
    
    RobotFound=False
    
    if len(hierarchy[0])>0:
        numObjetos=len(hierarchy[0])
        if numObjetos<50:
            for i,cnt in enumerate(contorno):
                
                M=cv2.moments(cnt)
                area=M["m00"]
                
                if area > MIN_AREA and area < MAX_AREA :
                    x=M["m10"]/area
                    y=M["m01"]/area
                    
                    r.SetPos(x,y)
                    r.setAngle(cnt)
                    r.setContorno(cnt)
                    RobotFound=True
                
                else:
                    RobotFound=False
            if RobotFound==True:
                DibujarRobot(r,frame)
            else:
                cv2.putText(frame,"MUCHO RUIDO AJUSTAR LOS FILTROS",(0,30),1,1,(0,0,255))
                
def DibujarRobot(r,frame):
    
    rect = cv2.minAreaRect(r.cnt)
    box = cv2.cv.BoxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(frame,[box],0,(255,0,0),2)
    
    cv2.putText(frame,"%s:%d , %d" % (r.nombre,r.posX,r.posY),(r.posX-10,r.posY),1,1,r.color)
    cv2.putText(frame,"Ang: %d" % (r.angulo),(r.posX-10,r.posY+20),1,1,r.color)
