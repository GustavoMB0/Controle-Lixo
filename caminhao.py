import json
from time import sleep
from types import SimpleNamespace
import socket
from _thread import *
import threading

from setor import Lixeira

class caminhao():
    nLixieras = 5
    ip = "" 
    lixeiras = []
    recolher = []
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, ip):
        self.ip = ip
        print("Caminhao inicializado")
        self.c.connect((ip, 30))
        

    
    def getLixeixa(self):
        msg = 'B'.encode()
        self.c.sendall(msg)
        data = self.c.recv(1024)
        data = data.decode("utf-8")
        j = json.loads(data)
        if data == "V" :
            return False 
        self.lixeiras = j
        return True             
    
    def exibir(self):
        print("Lixeiras: \n")
        for j in range(0, self.lixeiras.__len__()):
            lixeira = self.lixeiras[j]
            print(lixeira['setor'] + " " + lixeira['localizacao'] + ":  " + str(lixeira['ocupacao']) + "\n")

    def escolhe(self):
        print("Começou a escolher")
        lixeira = []
        msg = ""
        self.lixeiras.sort(key=lambda x: x['ocupacao'],  reverse= True)
        for i in range(0, self.nLixieras):
            if len(self.lixeiras[i]) == 0:
                print(self.lixeiras)
                lixeira = self.lixeiras.pop(0)
            else:
                break
        self.recolher = lixeira
        print("Definiu as lixeiras:")
        print(self.recolher)
        msg = "S".encode("utf-8")
        self.c.sendall(msg)
        data = self.c.recv(1024)
        data = data.decode("utf-8")
        if data == 'L':
            print('Setor livre')
            msg = "V".encode("utf-8")
            self.c.sendall(msg)
            j = json.dumps(self.lixeiras, default= lambda o: o.__dict__)
            self.c.sendall(j.encode("utf-8"))
            data = self.c.recv(1024)
            data = data.decode("utf-8")
            if data == "O":
                print("Começa a coleta")
                return True
            else:
                return False




    #Esvazia as lixeiras
    def esvaziar(self):
        self.exibir()
        for lixeira in self.recolher:
            if self.recolher != None:
                self.c.sendall("Z".encode())
                j = json.dumps(lixeira, default= lambda o: o.__dict__)
                self.c.sendall(j.encode())
                sleep(10)


if __name__ == '__main__':
    ip = input("Digite o ip: \n")
    caminhao = caminhao(ip)
    while(True):
        caminhao.getLixeixa()
        if(caminhao.escolhe()):
            print("Esvaziando")
            caminhao.esvaziar() 
            print("")           
        else:
            print("Aguardando setor...")
            sleep(10)

            


    
        

