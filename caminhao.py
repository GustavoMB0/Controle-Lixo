from ast import Return
from asyncio.windows_events import NULL
from distutils.command.clean import clean
import json
from time import sleep
from types import SimpleNamespace
import asyncio
import requests
import socket
from _thread import *
import threading

from setor import Lixeira

class caminhao():
    ip = "" 
    lixeiras = []
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, ip):
        self.ip = ip
        print("Caminhao inicializado")
        threading.Thread(target= self.listen, args=(self.s)).start()
    
    def getLixeixa(self, nLixeira):
        self.c.sendall('S')
        data  = self.c.recv(1024)
        if data == 'L':
            self.c.sendall('L'+nLixeira)
            data = self.c.recv(1024)
            self.lixeiras.append(json.load(data))
            return True             
        return False
    
    def exibir(self):
        print("Lixeiras: \n")
        for j in range(0, self.lixeiras.__len__()):
            lixeira = self.lixeiras[j]
            print(lixeira['setor'] + " " + lixeira['localizacao'] + ":  " + str(lixeira['ocupacao']) + "\n")

    
    #Criar rota de caminhao
    def esvaziar(self):
        self.lixeiras.sort(key=lambda x: x.ocupacao,  reverse= True)
        for l in range(0, 5):
            if(self.lixeiras[l] != NULL):
                print(self.lixeiras[l])        
                self.c.sendall(self.lixeiras[l])    
                sleep(5)            
        self.lixeiras = []
if __name__ == '__main__':
    ip = input("Digite o ip: \n")
    caminhao = caminhao(ip)
    while(True):
        if(caminhao.getLixeixa(10)):
            caminhao.esvaziar()            
        else:
            print("Aguardando setor...")
            sleep(5)

            


    
        

