import numpy as np
import pygame

class RobotS():
    def __init__(self,nombre,jugador):
        self.nombre=nombre
        self.jugador=jugador
        self.angulo=0
        self.anterior=0
        self.Front=0
        self.posX=0
        self.posY=0
        self.cnt=np.array([[[]]])
        self.status="Muerto"
        self.Asesino=["",""]
        self.imagen=0
        self.shotPos=(0,0)
        
        if self.nombre=="R1":
            self.HSV_MIN=np.array([[[18,83,0]]])
            self.HSV_MAX=np.array([[[58,243,174]]])
            self.color=(0,0,255)
            
        if self.nombre=="R2":
            self.HSV_MIN=np.array([[[18,83,0]]])
            self.HSV_MAX=np.array([[[58,243,174]]])
            self.color=(0,0,255)
         
        if self.nombre=="R3":
            self.HSV_MIN=np.array([[[18,83,0]]])
            self.HSV_MAX=np.array([[[58,243,174]]])
            self.color=(0,0,255)
            
    
    def graficar(self,pantalla,img,sprite,Sp_dic,status=None):
        diferencia= self.anterior-self.angulo
        
        self.anterior=self.angulo
        
        if diferencia>150 or diferencia<-150:
            
            if self.imagen == 0:
                self.imagen = 1
                
            else:
                self.imagen = 0         
                    
        sprite.rect=img[self.imagen].get_rect()
        sprite.rect.center=(self.posX,self.posY)  
        robot=pygame.transform.rotate(img[self.imagen],-self.angulo)
        pantalla.blit(robot,sprite.rect)
        
        if self.status != "Muerto":
            Sp_dic.update({self.jugador:sprite.rect})
                
        if status == "Apuntando":      
            pygame.draw.line(pantalla, (0,0,0), (self.posX,self.posY), (pygame.mouse.get_pos()), 3)
            pygame.draw.circle(pantalla, (255,0,0), (pygame.mouse.get_pos()), 10, 0)
            return status
        elif status == "Fuego":
            pygame.draw.line(pantalla, (0,0,0), (self.posX,self.posY), (self.shotPos), 3)
            pygame.draw.circle(pantalla, (255,0,0), (self.shotPos), 10, 0)
            return status
            
        elif status == "Analisis":
            pygame.draw.line(pantalla, (0,0,0), (self.posX,self.posY), (self.shotPos), 3)
            circulo=pygame.draw.circle(pantalla, (255,0,0), (self.shotPos), 10, 0)
            
            for nom in Sp_dic.keys():
                (Xs,Ys)=Sp_dic[nom].center
                (w,h)=Sp_dic[nom].size
                
                rectt=pygame.Rect(0,0,w+2*10,h+2*10)
                rectt.center=(Xs,Ys)
                if rectt.collidepoint(self.shotPos):
                    print "acerto",nom
                   
            return "detenido"


        
        
        
    
    #~ def SetPos(self,x,y):
        #~ self.posX=int(x)
        #~ self.posY=int(y)
        
    #def setAngle(self,cnt):
        #~ #rect = cv2.minAreaRect(cnt)
        #~ #angle=rect[2]
        #~ #if angle < 0:
        #~ #    angle=angle+180
        #~ #    
        #~ #self.angulo=angle
        #~ if len(cnt)<5:
            #~ pass
        #~ else:
            #~ (_,__),(___,____),angle = cv2.fitEllipse(cnt)
            #~ self.angulo=angle
        
    #def setContorno(self,contorno):
        #~ self.cnt=contorno
    
    
