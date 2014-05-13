from Robot import *
from ClassServer import *
from Camara import *
from ComandosSvV3 import *
import thread
import socket
import os
import cPickle as pickle
import time
import pygame

dic_comandos={"all":todos,"msj":msj,"init_datosR":init_datosR,"avansar":avansar,"girar_der":girar_der,"girar_isq":girar_isq,"parar":parar,"morir":morir,"start":start}

def comandos(Server):
    global dic_comandos
    Server.data=Server.msj.split()
    
    dic_comandos[Server.data[0]](Server)
    
    
def limpiar():
    os.system("cls")
    
def Conexion(host,port,Server):
    sock=socket.socket()
    sock.bind((host,port))
    #dic_sockets.update({"host":sock})
    while True:
        if len(Server.dic_sockets) == Server.maxJ:
            pass
        else:
            sock.listen(1)
            socket_cliente,datos_cliente=sock.accept()
            nombre=socket_cliente.recv(1024)
            list=[Server.nombre,Server.admin,Server.maxJ]
            data=pickle.dumps(list)
            longitud = len(data)
            socket_cliente.send(str(longitud))
            socket_cliente.send(data)
            Server.dic_sockets.update({nombre:socket_cliente})
            thread.start_new_thread(Entrada, (nombre,socket_cliente,Server))
    

def Entrada(nombre,socket,Server):
    while True:
        cantidad=socket.recv(1)
        longitud=socket.recv(int(cantidad))
        data=socket.recv(int(longitud))
        msj=pickle.loads(data)
        if msj == "listo":
            for r in Server.listaR:
                if r.jugador == nombre:
                    r.status = "listo" 
                    
                    
        elif msj[0] == "status":
            pass
        #status del robot
                    
        elif msj[0] == "Fuego":
            for r in Server.listaR:
                if r.jugador == nombre:
                    r.status = "Fuego"
                    thread.start_new_thread(Server.Analisis,(nombre,msj[1],msj[2]))
                    
        
        else:
            pass
        
def main():
    Server=ServerGame()
    Server.mainloop=True
    while Server.mainloop == True:
        while True:
            print "\t\tBienvenido al Server Lucha de Robots (V2.0)"
            print "Menu:"
            print "\n1-Set Mode"
            print "2-Server"
            print "\n\n0-Salir"
            
            opcion=input(">>> ")
            
            if opcion == 1:
                Server.setmode=True
            elif opcion == 2:
                Server.servermode=True
            elif opcion == 0:
                Server.mainloop=False
                break
            
            if Server.setmode == True:
                pass
            
            elif Server.servermode == True:
                
                admin= raw_input("\nIngrese su usuario: ")
                host= raw_input("\nIngrese su ip de host: ")
                port=9999
                
                nomSv= raw_input("\nIngrese un nombre para su Servidor: ")
                
                maxJ= input("\nIngrese el maximo de jugadores para comensar: ")
                
                Server.admin=admin
                Server.nombre=nomSv
                Server.maxJ=maxJ
                
                thread.start_new_thread(Conexion, (host,port,Server))
                thread.start_new_thread(datosR, (Server,))
                
                jugadores=0
                
                while maxJ != jugadores:
                    limpiar()
                    time.sleep(0.1)
                    jugadores=len(Server.dic_sockets)
                    print "\t\t",Server.nombre
                    print "\nAdmin:",Server.admin
                    print "Host:",host
                    print "\n Jugadores conectados: %d/%d" % (jugadores,Server.maxJ)
                    
                    Server.listaJ=Server.dic_sockets.keys()
                
                    
                    for i in range(0,Server.maxJ):
                        if len(Server.listaJ)<i+1:
                            print "\n R%d: ---" % (i+1)
                        else:
                            print "\n R%d: %s" % (i+1,Server.listaJ[i])
                            r=RobotS("R%d" % (i+1),Server.listaJ[i])
                            Server.listaR.append(r)
                            
                
                raw_input("Jugadores listos, Enter para comensar la configuracion...")

                
                limpiar()
                print "\t\t",nomSv
                thread.start_new_thread(camara, (Server,))
                print "Camaras iniciadas.."
                
                
                raw_input("Enter para iniciar el control manual del servidor...")
                limpiar()
                
                
                while True:
                    print "\t\t",Server.nombre
                    print "\nAdmin:",Server.admin
                    print "Host:",host
                    print "\nJugadores:"
                    for i,nom in enumerate(Server.listaJ):
                        print "R%d: %s" % (i+1,nom)
                    
                    print "Bienvenido, abajo tiene todos los comandos y sus funciones: "
                    #agregar comandos##
                    
                    Server.msj=raw_input(">>> ")
                    
                    comandos(Server)
                    limpiar()
                
main()