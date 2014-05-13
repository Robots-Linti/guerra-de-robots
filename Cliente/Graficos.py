import pygame
import thread
import time
from ClassServer import *
from Robot import *
from Robot_cliente import *


def imgLoad(r):
    if r.status == "Muerto":
        img1=pygame.image.load("destruido_1.png")
        img2=pygame.image.load("destruido_2.png")
        
    else:
        img1=pygame.image.load("%s_1.png" % (r.nombre))
        img2=pygame.image.load("%s_2.png" % (r.nombre))
        
    return [img1,img2]
    
    
    


def Movimientos(botones,Robott):
    
    if botones[pygame.K_w] and botones[pygame.K_d]:
        Robott.status = "Avansado y girando (der)"
        Robott.avansar()
        
    elif botones[pygame.K_w] and botones[pygame.K_a]:
        Robott.status = "Avansado y girando (isq)"
        Robott.avansar()
        
    elif botones[pygame.K_w]: 
        Robott.status = "Avansado"
        Robott.avansar()
    
    
    elif botones[pygame.K_d]: 
        Robott.status = "girando (der)"
        Robott.girar_der()
        
    elif botones[pygame.K_a]:
        Robott.status = "girando (isq)"
        Robott.girar_isq()
    
    elif botones[pygame.K_s]:
        Robott.status = "Reversa"
        Robott.reversa()
        
    else:
        Robott.status="detenido"
        Robott.parar()
    

def Tiempo(time,tiempo):
    
    if tiempo[4] != time:
        tiempo[3]+=1
    
    if tiempo[3] == 10:
        tiempo[2]+=1
        tiempo[3]=0
    
    if tiempo[2] == 6:
        tiempo[1]+=1
        tiempo[2]=0
    
    if tiempo[1] == 10:
        tiempo[0]+=1
        tiempo[1]=0
        
    tiempo[4]=time
    
    return tiempo
    

def Graficos(Server):
    Server.graficos=True          
    pygame.init()
    pantalla=pygame.display.set_mode((640,380))
    salir=False
    f1=pygame.font.SysFont("Arial", 20, True, False)
    NomSv=f1.render(Server.nombre,0,(0,0,0))
    Game=f1.render("Game:",0,(0,0,0))
    sprite=pygame.sprite.Sprite()
    
    tiempo=[0,0,0,0,0]
    
    clock= pygame.time.Clock()
    while salir !=True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir=True
                
                
        clock.tick(60)
        pantalla.fill((255,255,255))
        pygame.draw.rect(pantalla,(0,0,0),(5,50,325,320))
        pygame.draw.rect(pantalla,(255,255,255),(10,55,315,310))
        pygame.draw.rect(pantalla, (0,0,0),(335,220,300,150))
        pygame.draw.rect(pantalla,(255,255,255),(340,225,290,140))
        pantalla.blit(NomSv,(286,5))
        pantalla.blit(Game,(5,29))
        
        if Server.juego != True:
            adv=f1.render("Esperando a todos los jugadores...",0,(150,150,150))
            pantalla.blit(adv,(5,5))
        
        else:
        
            time=(pygame.time.get_ticks()/1000)
            
            tiempo=Tiempo(time,tiempo)
            Server.Tiempo=tiempo
            
        algo=f1.render("Tiempo: %d%d:%d%d " % (tiempo[0],tiempo[1],tiempo[2],tiempo[3]),0,(0,0,0))
        pantalla.blit(algo,(515,5))
        
        Px=356
        Py=58
        
        Server.Sp_dic={}
        
        for r in Server.listaR:
            if r.status == "Muerto":
                Jugador=f1.render("%s: (DESTRUIDO) %s (%s) " % (r.nombre,r.Asesino[0],r.Asesino[1]),0,(0,0,0))
                pantalla.blit(Jugador,(Px,Py))
                img=[]
                img=imgLoad(r)
                r.graficar(pantalla,img,sprite,Server.Sp_dic)
                Py+=20
                
            else:
                
                Jugador=f1.render("%s: %s   (%d,%d) (Ang: %d)" % (r.nombre,r.jugador,r.posX,r.posY,r.angulo),0,(0,0,0))
                pantalla.blit(Jugador,(Px,Py))
                img=[]
                img=imgLoad(r)
                r.graficar(pantalla,img,sprite,Server.Sp_dic)
                Py+=20
        
        pygame.display.update()
    pygame.quit()
        
def Graficos_Cliente(Server,Robott):
    
    Server.graficos=True          
    pygame.init()
    pantalla=pygame.display.set_mode((690,380))
    salir=False
    f1=pygame.font.SysFont("Arial", 20, True, False)
    NomSv=f1.render(Server.nombre,0,(0,0,0))
    Game=f1.render("Game:",0,(0,0,0))
    sprite=pygame.sprite.Sprite()
    
    tiempo=[0,0,0,0,0]
    
    clock= pygame.time.Clock()
    while salir !=True:
        if Server.juego != True:
            pass
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    salir=True
                    
                if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:
						print "boton"
						if Robott.status == "Apuntando":
							Robott.status = "detenido"
							
						elif Robott.status == "Fuego" or Robott.status == "Muerto":
							pass
						
						else:
							Robott.status = "Apuntando"
							Robott.parar()
							print "cambie"
							print Robott.status
                            
                elif event.type == pygame.MOUSEBUTTONDOWN and Robott.status == "Apuntando":
					print "aprete"
					mouse=pygame.mouse.get_pressed()
					if mouse[0]:
						Robott.shotPos=pygame.mouse.get_pos()
						Robott.status="Fuego"
						thread.start_new_thread(Robott.disparar, (Server,))
    
                if (Robott.status != "Muerto"  
                    and Robott.status != "Apuntando" 
                    and Robott.status != "Fuego" 
                    and Robott.status != "Analisis"):
                    
                    pygame.event.pump()
                    botones=pygame.key.get_pressed()
                    Movimientos(botones,Robott)
                
        clock.tick(60)
        pantalla.fill((255,255,255))
        pygame.draw.rect(pantalla,(0,0,0),(5,50,325,320))
        pygame.draw.rect(pantalla,(255,255,255),(10,55,315,310))
        #pygame.draw.rect(pantalla, (0,0,0),(335,220,300,150))
        #pygame.draw.rect(pantalla,(255,255,255),(340,225,290,140))
        
        
        
        pantalla.blit(NomSv,(286,5))
        pantalla.blit(Game,(5,29))
        
        if Server.juego != True:
            adv=f1.render("Esperando a todos los jugadores...",0,(150,150,150))
            pantalla.blit(adv,(5,5))
        
        else:
        
            times=(pygame.time.get_ticks()/1000)
            
            tiempo=Tiempo(times,tiempo)
            Server.Tiempo=tiempo
                
        algo=f1.render("Tiempo: %d%d:%d%d " % (tiempo[0],tiempo[1],tiempo[2],tiempo[3]),0,(0,0,0))
        pantalla.blit(algo,(515,5))
        
        Px=356
        Py=58
        
        Server.Sp_dic={}
        
        for r in Server.listaR:
            if r.status == "Muerto":
                Jugador=f1.render("(DESTRUIDO) %s (%s) " % (r.Asesino[0],r.Asesino[1]),0,(0,0,0))
                pantalla.blit(Jugador,(Px,Py))
                img=[]
                img=imgLoad(r)
                r.graficar(pantalla,img,sprite,Server.Sp_dic)
                Py+=20
                
            else:
                
                Jugador=f1.render("%s: %s   (%d,%d) (Ang: %d)" % (r.nombre,r.jugador,r.posX,r.posY,r.angulo),0,(0,0,0))
                pantalla.blit(Jugador,(Px,Py))
                img=[]
                img=imgLoad(r)
                r.graficar(pantalla,img,sprite,Server.Sp_dic)
                Py+=20
            
        for r in Server.listaR:
            if r.jugador == Robott.nombre:
                if Robott.status == "Apuntando" or Robott.status == "Fuego" \
                                                or Robott.status == "Analisis":
                    r.shotPos=Robott.shotPos
                    r.status=Robott.status
                    
                    Robott.status=r.graficar(pantalla,img,sprite,Server.Sp_dic,Robott.status)
                
            else:
                pass
            
        pygame.display.update()
    pygame.quit()
