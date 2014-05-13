import pygame
import time
import cPickle as pickle

class ServerGame(object):
    def __init__(self):
        self.mainloop=False
        self.setmode=False
        self.servermode=False
        self.Game=False
        self.sock=None
        self.nombre=""
        self.admin=""
        self.maxJ=0
        self.juego=False
        self.graficos=False
        self.camara=False
        self.Tiempo=[0,0,0,0]
        self.msj=""
        self.error=""
        self.data=[]
        self.listaJ=[]
        self.dic_sockets={}
        self.Sp_dic={}
        self.listaR=[]
        self.atributos={"game":self.Game,"graficos":self.graficos,"camara":self.camara}
        
    def Analisis(self,jugador,Tf,shotPos):
        
        Ti=time.time()
        Tf=Tf+Ti
        
        while Ti < Tf :
            Ti=time.time()
        
        for nom in self.Sp_dic.keys():
            (Xs,Ys)=self.Sp_dic[nom].center
            (w,h)=self.Sp_dic[nom].size
            
            rectt=pygame.Rect(0,0,w+2*10,h+2*10)
            rectt.center=(Xs,Ys)
            if rectt.collidepoint(shotPos):
                for r in self.listaR:
                    if r.jugador == nom:
                        r.status = "Muerto"
                        Tiempo="%d%d:%d%d" % (self.Tiempo[0],self.Tiempo[1],self.Tiempo[2],self.Tiempo[3])
                        r.Asesino=[Tiempo,jugador]
                        
                data=["Destruido"]
                data=pickle.dumps(data)
                longitud=len(data)
                cantidad=len(str(longitud))
                self.dic_sockets[nom].send(str(cantidad))
                self.dic_sockets[nom].send(str(longitud))
                self.dic_sockets[nom].send(data)
                
            for r in self.listaR:
                if r.jugador == jugador:
                    if r.status != "Muerto":
                
                        data=["status","detenido"]
                        data=pickle.dumps(data)
                        longitud=len(data)
                        cantidad=len(str(longitud))
                        self.dic_sockets[jugador].send(str(cantidad))
                        self.dic_sockets[jugador].send(str(longitud))
                        self.dic_sockets[jugador].send(data)
                    
                    
                    
                    
                    