import socket
import cPickle as pickle
import thread
import time
from Graficos import Graficos
from Camara import *



def start(Server):
    dic_func={"camara":init_camara,"graficos":init_Graficos,"datosR":init_datosR,"game":init_Game}
    
    if Server.atributos[Server.data[1]] == True:
        pass
    else:
        dic_func[Server.data[1]](Server)

def init_datosR(Server):
    thread.start_new_thread(datosR, (Server,))
    
def init_camara(Server):
    thread.start_new_thread(camara,(Server,))

def init_Graficos(Server):
    thread.start_new_thread(Graficos, (Server,))
    
def init_Game(Server):
    thread.start_new_thread(Game, (Server,))

def datosR(Server):
    while True:
        if Server.listaR == []:
            pass
        else:
            for r in Server.listaR:
                data=["datos",Server.listaR,Server.listaJ,Server.Game,Server.juego]
                data=pickle.dumps(data)
                longitud=len(data)
                cantidad=len(str(longitud))
                #print longitud,cantidad
                Server.dic_sockets[r.jugador].send(str(cantidad))
                Server.dic_sockets[r.jugador].send(str(longitud))
                #time.sleep(0.01)
                Server.dic_sockets[r.jugador].send(data)
            
            time.sleep(0.08)

def todos(Server):
    data=pickle.dumps(Server.data[1:])
    longitud=len(data)
    for nom in Server.dic_sockets.keys():
            Server.dic_sockets[nom].send(str(longitud))
            Server.dic_sockets[nom].send(data)
            
def msj(Server):
    data=pickle.dumps(Server.data[2:])
    longitud=len(data)
    for nom in Server.data[1:]:
        Server.dic_sockets[nom].send(str(longitud))
        Server.dic_sockets[nom].send(data)
        
        
def avansar(Server):
    try:
        for nom in Server.data[1:]:
            msj=pickle.dumps("avansar")
            longitud=len(msj)
            Server.dic_sockets[nom].send(str(longitud))
            Server.dic_sockets[nom].send(msj)
    except:
        print "error jugador",nom,"no existe"
        
def girar_der(Server):
    
    try:
        for nom in Server.data[1:]:
            msj=pickle.dumps("girar_der")
            longitud=len(msj)
            Server.dic_sockets[nom].send(str(longitud))
            Server.dic_sockets[nom].send(msj)
    except:
        print "error jugador",nom,"no existe"
    
def girar_isq(Server):
    
    try:
        for nom in Server.data[1:]:
            msj=pickle.dumps("girar_isq")
            longitud=len(msj)
            Server.dic_sockets[nom].send(str(longitud))
            Server.dic_sockets[nom].send(msj)
    except:
        print "error jugador",nom,"no existe"
    
def disparar(Server):
    
    try:
        for nom in Server.data[1:]:
            msj=pickle.dumps("disparar")
            longitud=len(msj)
            Server.dic_sockets[nom].send(str(longitud))
            Server.dic_sockets[nom].send(msj)
    except:
        print "error jugador",nom,"no existe"

def morir(Server):
    try:
        for nom in Server.data[1:]:
            msj=pickle.dumps("morir")
            longitud=len(msj)
            Server.dic_sockets[nom].send(str(longitud))
            Server.dic_sockets[nom].send(msj)
    except:
        print "error jugador",nom,"no existe"
        
def parar(Server):
    try:
        if Server.data[1] == "all":
            for nom in Server.dic_sockets.keys():
                msj=pickle.dumps("parar")
                longitud=len(msj)
                Server.dic_sockets[nom].send(str(longitud))
                Server.dic_sockets[nom].send(msj)
        else:
            for nom in Server.data[1:]:
                msj=pickle.dumps("parar")
                longitud=len(msj)
                Server.dic_sockets[nom].send(str(longitud))
                Server.dic_sockets[nom].send(msj)
    except:
        print "error jugador",nom,"no existe"

def iniciar(Server):
    for nom in Server.dic_sockets.keys():
        msj=pickle.dumps("iniciar")
        longitud=len(msj)
        Server.dic_sockets[nom].send(str(longitud))
        Server.dic_sockets[nom].send(msj)
        Server.Game=True
        thread.start_new_thread(Game,(Server,))
        
def Game(Server):
    Server.Game=True
    thread.start_new_thread(Graficos, (Server,))
    Server.juego= False
    pendientes = []
    while Server.juego != True:
        for r in Server.listaR:
            if r.status == "listo":
                pass
            else:
                pendientes.append(r)
        
        if pendientes == []:
            Server.juego = True
        else:
            pendientes = []
        

            
    
