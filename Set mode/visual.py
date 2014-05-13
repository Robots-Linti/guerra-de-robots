import cv2
import numpy as np

class Figuras():
    def __init__(self,nombre):
        self.nombre=nombre
        self.PosX=0
        self.PosY=0
        ### edit###
        
        self.angulo=0
        self.lefY=0
        self.rigY=0
        
        ### edit###
        
        if self.nombre=="Robot":
            self.HSV_MIN=np.array([[[43,69,14]]])
            self.HSV_MAX=np.array([[[69,194,245]]])
            self.color=(255,255,255)
        
        if self.nombre=="Triangulo":
            self.HSV_MIN=np.array([[[145,89,75]]])
            self.HSV_MAX=np.array([[[179,255,216]]])
            self.color=(0,0,255)
            
        if self.nombre=="Cuadrado":
            self.HSV_MIN=np.array([[[48,139,109]]])
            self.HSV_MAX=np.array([[[67,255,255]]])
            self.color=(0,255,0)
            
        if self.nombre=="Circulo":
            self.HSV_MIN=np.array([[[113,101,101]]])
            self.HSV_MAX=np.array([[[131,234,202]]])
            self.color=(255,0,0)
        
    def SetPos(self,x,y):
        self.PosX=int(x)
        self.PosY=int(y)
    
    def SetAngle(self,cnt):
        rect = cv2.minAreaRect(cnt)
        angle=rect[2]
        self.angulo=angle
        
    def SetFitLine(self,cnt):
        
        vx,vy,x,y = cv2.fitLine(cnt[2],cv2.cv.CV_DIST_L2,0,0.01,0.01)
    
        lefty = int((-x*vy/vx) + y)
        righty = int(((cnt[2].shape[1]-x)*vy/vx)+y)
        
        self.lefY=lefty
        self.rigY=righty
    
        

def paso(int,):
    pass
    

def crearbarras():
    H_MIN = 0
    H_MAX = 179
    S_MIN = 0
    S_MAX = 255
    V_MIN = 0
    V_MAX = 255

    trackbarWindowName="HSV RANGE"
    cv2.namedWindow(trackbarWindowName,0)
    cv2.resizeWindow(trackbarWindowName, 300,300)
    #cv2.createTrackbar("umbral" , "threshold", slider,slider_max,paso)
    #cv2.createTrackbar("range","threshold",slider2,slider_max,paso)
    cv2.createTrackbar( "H_MIN", trackbarWindowName, H_MIN, H_MAX, paso )
    cv2.createTrackbar( "H_MAX", trackbarWindowName, H_MAX, H_MAX, paso )
    cv2.createTrackbar( "S_MIN", trackbarWindowName, S_MIN, S_MAX, paso )
    cv2.createTrackbar( "S_MAX", trackbarWindowName, S_MAX, S_MAX, paso )
    cv2.createTrackbar( "V_MIN", trackbarWindowName, V_MIN, V_MAX, paso )
    cv2.createTrackbar( "V_MAX", trackbarWindowName, V_MAX, V_MAX, paso )
    
def morpho(th1):
    kernel1=np.ones((3,3),np.uint8)
    kernel2=np.ones((4,4),np.uint8)
    th1=cv2.erode(th1,kernel1,iterations=1)
    th1=cv2.dilate(th1,kernel2,iterations=1)
    return th1
def seguimiento_figuras(figura,th1,hsv,frame):
    lista_Fig=[]
    MIN_AREA=20*20
    MAX_AREA=150*150
    temp=th1.copy()
    contorno,hierarchy=cv2.findContours(temp,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    if hierarchy==None:
        hierarchy=np.array([[[]]])
    #print "hie:",len(hierarchy[0])
    refArea=0
    objectFound=False
    if len(hierarchy[0])>0:
        numObjetos=len(hierarchy[0])
        if numObjetos<50:
            for i,cnt in enumerate(contorno):
               
                fig=Figuras("nada")
                
                M=cv2.moments(cnt)
                area=M["m00"]
                    
                if area > MIN_AREA and area < MAX_AREA :
                    x=M["m10"]/area
                    y=M["m01"]/area
                    fig.SetPos(x,y)
                    fig.nombre=figura.nombre
                    
                    ### edit ###
                    fig.SetAngle(cnt)
                    fig.SetFitLine(cnt)
                    ### edit ###
                    
                    lista_Fig.append(fig)
                    objectFound=True
                    
                else:
                    objectFound=False
                
            if objectFound==True:
                dibujarFigura(lista_Fig,frame)
        else:
            cv2.putText(frame,"MUCHO RUIDO AJUSTAR LOS FILTROS",(0,30),1,1,(0,0,255))
            
def seguimiento_objeto(th1,hsv,frame):
    MIN_AREA=20*20
    MAX_AREA=150*150
    x,y=0,0
    temp=th1.copy()
    contorno,hierarchy=cv2.findContours(temp,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    if hierarchy==None:
        hierarchy=np.array([[[]]])
    print "hie:",len(hierarchy[0])
    refArea=0
    objectFound=False
    if len(hierarchy[0])>0:
        numObjetos=len(hierarchy[0])
        if numObjetos<50:
            for i,cnt in enumerate(contorno):
                #index=hierarchy[index][0]
                M=cv2.moments(cnt)
                area=M["m00"]
                    
                if area > MIN_AREA and area < MAX_AREA :
                    x=M["m10"]/area
                    y=M["m01"]/area
                    objectFound=True
                
                else:
                    objectFound=False
                
                if objectFound==True:
                    dibujarObjeto(x,y,frame,i)
        else:
            cv2.putText(frame,"MUCHO RUIDO AJUSTAR LOS FILTROS",(0,30),1,1,(0,0,255))
def dibujarObjeto(x,y,frame,i):

    cv2.circle(frame,(int(x),int(y)),10,(0,255,0))
    cv2.putText(frame,"%d,%d Objeto %d" % (x,y,i),(int(x),int(y)+20),1,1,(0,0,255))

def dibujarFigura(lista_Fig,frame):
    for ffigura in lista_Fig:
        
        cv2.circle(frame,(ffigura.PosX,ffigura.PosY),10,(0,255,0))
        cv2.putText(frame,"%d,%d %s" % (ffigura.PosX,ffigura.PosY,ffigura.nombre),(ffigura.PosX,ffigura.PosY+20),1,1,(0,0,255))

        ### edit  ###
        cv2.line(frame,(ffigura.PosX,ffigura.PosY),(0,ffigura.lefY),(0,255,0),1,cv2.CV_AA)
        cv2.putText(frame,"Angulo %d" % (ffigura.angulo),(ffigura.PosX,ffigura.PosY+40),1,1,(255,255,255))
        
    

def main():

    ModoAjuste=True
    img=cv2.VideoCapture(0)
    crearbarras()
    trackbarWindowName="HSV RANGE"
    img.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,600)
    img.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,600)
    cv2.namedWindow("asds",0)
    cv2.resizeWindow("asds", 600,420)
    while True:
        _, frame = img.read()
        if ModoAjuste==True:           
            H_MIN = cv2.getTrackbarPos("H_MIN", trackbarWindowName) 
            H_MAX = cv2.getTrackbarPos("H_MAX", trackbarWindowName) 
            S_MIN = cv2.getTrackbarPos("S_MIN", trackbarWindowName) 
            S_MAX = cv2.getTrackbarPos("S_MAX", trackbarWindowName) 
            V_MIN = cv2.getTrackbarPos("V_MIN", trackbarWindowName) 
            V_MAX = cv2.getTrackbarPos("V_MAX", trackbarWindowName)
            hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            th1=cv2.inRange(hsv,np.array([[[H_MIN,S_MIN,V_MIN]]]),np.array([[[H_MAX,S_MAX,V_MAX]]]))
            th1=morpho(th1)
            seguimiento_objeto(th1,hsv,frame)
        else:
            
            Robot=Figuras("Robot")
            hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            th1=cv2.inRange(hsv,Robot.HSV_MIN,Robot.HSV_MAX)
            th1=morpho(th1)
            
            seguimiento_figuras(Robot,th1,hsv,frame)
            
            #Triangulo=Figuras("Triangulo")
            #hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            #th1=cv2.inRange(hsv,Triangulo.HSV_MIN,Triangulo.HSV_MAX)
            #th1=morpho(th1)
            #seguimiento_figuras(Triangulo,th1,hsv,frame)
            
            #Cuadrado=Figuras("Cuadrado")
            #hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            #th1=cv2.inRange(hsv,Cuadrado.HSV_MIN,Cuadrado.HSV_MAX)
            #th1=morpho(th1)
            #seguimiento_figuras(Cuadrado,th1,hsv,frame)
            
            #Circulo=Figuras("Circulo")
            #hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            #th1=cv2.inRange(hsv,Circulo.HSV_MIN,Circulo.HSV_MAX)
            #th1=morpho(th1)
            #seguimiento_figuras(Circulo,th1,hsv,frame)
        
        cv2.imshow("asds",frame)
        
        cv2.imshow("asd",th1)
        #slider,slider2=0,20
        #slider_max=170
        #cv2.namedWindow("threshold",1)
        #barra2(slider2) 
        
        cv2.waitKey(1)
        
    
main()