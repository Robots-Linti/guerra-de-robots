from duinobot import *
from Robot_cliente import *
from ClassServer import *
from Graficos import *
import socket
import os
import time
import thread
import cPickle as pickle

def limpiar():
    os.system('clear')

def datos(data,Robott,Server):
    
    Server.listaR=data[1]
    Server.listaJ=data[2]
    Server.Game=data[3]
    Server.juego=data[4]
    
    for r in Server.listaR:
        if r.jugador==Robott.nombre:
            Robott.angulo=r.angulo
        else:
            pass
    
def mensaje(msj):
    print (" ").join(msj)
    
def Entrada(sock,Robott,r,Server):
    while True:
        cantidad=sock.recv(1)
        longitud=sock.recv(int(cantidad))
        data=sock.recv(int(longitud),socket.MSG_WAITALL)
        msj=pickle.loads(data)
        if msj[0] == "datos":
            thread.start_new_thread(datos,(msj,Robott,Server))
        
        elif msj[0] == "mensaje":
            mensaje(msj[1:])
            
        elif msj[0] == "status":
			Robott.status=msj[1]
			r.status=msj[1]
        
        else:
            Robott.comandos[msj[0]]()
        
def main():
    print "\t\t Guerra de Robots cliente(v2.0)"
    nom=raw_input( "\nIngrese su nombre: ")
    id=input( "\nId de su robot: ")
    
    b=Board("/dev/ttyUSB0")
    r=Robot(b,id)
    Robott=RobotC(nom,id,r)
    
    host=raw_input("Ingrese la direccion del servidor: ")
    port=9999
    
    sock=socket.socket()
    sock.connect((host,port))
    sock.send(nom)
    
    Server=ServerGame()
    
    longitud=sock.recv(2)
    data=sock.recv(int(longitud))
    msj=pickle.loads(data)
    
    Server.nombre=msj[0]
    Server.admin=msj[1]
    Server.maxJ=msj[2]
    Server.sock=sock
    
    thread.start_new_thread(Entrada, (sock,Robott,r,Server))
    jugadores=0

    while Server.maxJ != jugadores:
        limpiar()
        time.sleep(0.1)
        jugadores=len(Server.listaJ)
        print "\t\t",Server.nombre
        print "\nAdmin:",Server.admin
        print "Host:",host
        print "\n Jugadores conectados: %d/%d" % (jugadores,Server.maxJ)
        
        for i in range(0,Server.maxJ):
            if len(Server.listaJ)<i+1:
                print "\n R%d: ---" % (i+1)
            else:
                print "\n R%d: %s" % (i+1,Server.listaJ[i])
    
    while True:
        if Server.Game == False:
			limpiar()
			print Server.Game
			print "\t\t",Server.nombre
			print "\nAdmin:",Server.admin
			print "Host:",host
			print "\nJugadores:"
			for i,nom in enumerate(Server.listaJ):
				print "R%d: %s" % (i+1,nom)
				
			print "Esperando al servidor para comensar el juego..."  
			
			time.sleep(0.1)
        
        else:
            Robott.status="detenido"
            thread.start_new_thread(Graficos_Cliente,(Server,Robott))
            
            data="listo"
            data=pickle.dumps(data)
            longitud=len(data)
            cantidad=len(str(longitud))
            Server.sock.send(str(cantidad))
            Server.sock.send(str(longitud))
            Server.sock.send(data)
            
            print Server.Game
            while Server.Game != False:
                pass
            
            
main()
