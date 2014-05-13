from duinobot import *
import numpy as np
import time
import cPickle as pickle

class RobotC():
    def __init__(self,nombre,ide,control):
        self.nombre=nombre
        self.id=ide
        self.control=control
        self.frente=0
        self.posX=0
        self.posY=0
        self.angulo=0
        self.shotPos=(0,0)
        self.status="Muerto"
        #if self.status == "Lock" or "Detenido" or "Muerto" or "Avansando":
        #    self.velocidad=(30,30)
        
        self.comandos={"avansar":self.avansar,"girar_der":self.girar_der,"girar_isq":self.girar_isq,"disparar":self.disparar,"Destruido":self.morir}
        self.list_com=[self.avansar,self.girar_der,self.girar_isq,self.disparar]
        
    def avansar(self):
		der,isq=30,30
		if self.status == "Avansado":
			der,isq = (30,30)
			
		elif self.status == "Avansado y girando (der)":
			der,isq = (30,40)
		
		elif self.status == "Avansado y girando (isq)":
			der,isq = (40,30)
		
		self.control.motors(der,isq)
            
    def girar_der(self):
        der,isq=30,30
        if self.status == "girando (der)":
            der,isq = (-30,30)
        
        if self.status == "Avansado y girando (der)":
             der,isq = (30,40)
             
        self.control.motors(der,isq)
    
    def girar_isq(self):
		der,isq=30,30
		if self.status == "girando (isq)":
			der,isq = (30,-30)
		
		if self.status == "Avansado y girando (isq)":
			 der,isq = (40,30)
			 
		self.control.motors(der,isq)
        
    def reversa(self):
		der,isq=30,30
		if self.status == "Reversa":
			der,isq=-30,-30
		self.control.motors(der,isq)
        
            
    def disparar(self,Server):
        difx=self.posX-self.shotPos[0]
        dify=self.posY-self.shotPos[1]
        if difx < 0: difx=-difx
        if dify < 0: dify=-dify
        
        diferencia=int(np.sqrt(difx**2+dify**2))
        Tf=(diferencia/10)*0.1
        #Tf=Ti+Tf
        #print self.posX,self.shotPos[0]
        #print "Diferencia:",diferencia,"Ti:",Ti,"Tf:",Tf 
        
        data=["Fuego",Tf,self.shotPos]
        data=pickle.dumps(data)
        longitud=len(data)
        cantidad=len(str(longitud))
        Server.sock.send(str(cantidad))
        Server.sock.send(str(longitud))
        Server.sock.send(data)
                
        #self.status="Analisis"
        
    
    def morir(self):
        self.status = "Muerto"
        self.control.stop()
        
    
    def parar(self):
		self.control.stop()
