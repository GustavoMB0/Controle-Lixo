from concurrent.futures import thread
from pickle import TRUE
from pyclbr import Class
import paho.mqtt.client as mqtt
import re
import json
from time import sleep
import socket
from _thread import *
import threading

#
# Alterar myip e ip os ips correto atualmente funcional apenas no localhost
#
class Setor:

    HOST = '127.0.0.1'
    PORT = 30 #REVIEW Definir porta para conexão
    myip = "localhost" #REVIEW botar o ip da maquina na rede
    ip = "localhost"
    setores = []
    name = ""
    ocupado = False
    lixeiras = []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, name):
        self.name = name
        self.sendMQtt()
        self.s.bind((self.HOST, self.PORT))
        threading.Thread(target= self.listen, args=(self.s)).start()

    def sendMQtt(self):
        message = {"nome" : self.name, "ip" : self.myip}
        print(message)

    #Metodo para conectar e se comunicar com os outros setores
    def connect(self):
        s=socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto({'name': self.name, 'addr': self.myip}, ('255.255.255.255', self.PORT))
        s.close()

    def listen(self):
        self.s.listen()
        while True:
            conn, addr = self.s.accept()
            conn.settimeout(80)
            threading.Thread(target = self.listenToClient, args=(conn, addr)).start()

    def listenToClient(self, conn, addr):
        while True:
            data = conn.recv(1024)
            conn, addr = self.s.accept()
            if data == 'S':
                if not self.ocupado:
                    conn.sendall("L")
                else:
                    conn.sendall("O")
            elif data == "k":
                data = conn.recv(1024)
                self.lixeiras.remove(data, key = lambda x: x.localizacao)
            elif re.source("name", data):
                if not self.setores.count(data, key = lambda x: x.name):
                    self.setores.append(data)
            elif re.source("localizacao", data):
                if not self.lixeiras.count(data, key = lambda x: x.localizacao):
                    client.publish(self.ip+"/"+data.localizacao, "E")
                    for setor in self.setores:
                            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            c.connect(setor.ip, self.PORT)
                            c.sendall("K")
                            c.sendall(data)
                            c.close()           
                else:
                    for x in self.setores:
                        if(data.setor == x.nome):
                            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            c.connect(x.ip, self.PORT)
                            c.sendall(data)
                            c.close()
            elif data == "x":
                data = conn.recv(1024)
                for recebida in data:
                    if not self.lixeiras.count(recebida, key = lambda x: x.localizacao):
                        self.lixeiras.append(recebida)
                    else:
                        for i in range(0, self.lixeiras):
                            if self.lixeiras[i].localizacao == recebida.localizacao:
                                self.lixeiras[i] == recebida
            elif re.search("^L[0-9]+$", data):#REVIEW mudar para mandar todas as lixeiras
                nLixeira = int(data.split("L"))
                conn.sendall(self.getLixeira(nLixeira))

    #Pega as lixeiras para mandar para o caminhão
    def getLixeira(self, nLixeira):
        listLixeira = []
        if nLixeira <= self.lixeiras.count():
            self.lixeiras.sort(key=lambda x: x.ocupacao,  reverse= True)
            for i in range (0, nLixeira):
                if self.lixeiras[i].setor != self.name:
                    self.c.sendall('S')
                    data  = self.c.recv(1024)
                    if(data == "L"):
                        listLixeira.append(self.lixeiras[i])
                else:
                    listLixeira.append(self.lixeiras[i])    
            
        #ANCHOR Tratar quando o setor não tiver o numero de lixeiras necessario 
        return json.dumps(listLixeira, default=lambda o: o.__dict__)

    def writeJson(self):
        with open("test.json", "w") as out:
            json.dump(self.lixeiras, out, default=lambda o: o.__dict__)
    
    #
    def gerenciaLixo(self, lixeiras, comando, Lixeira):
        if comando == 1:
            #Verificar se existe para adicionar lixo
            for x in lixeiras:
                if Lixeira.localizacao == x.localizacao:
                    x.ocupacao = Lixeira.ocupacao
        elif comando == 2:
            #Alterar o estado para travada
            for i in lixeiras:
                if i.name == Lixeira.name:
                    if not i.travado:
                        i.travado == True
                    else:
                        i.travado == False


    def addLixeira(self, Lixeira):
        if sum(map(lambda x: x.localizacao == Lixeira.localizacao, self.lixeiras)) == 0:
            self.lixeiras.append(Lixeira)
            self.lixeiras.sort(key=lambda x: x.ocupacao,  reverse= True)
            return 1
        else:
            return -1
    def sendLixeiras(self):
        for x in self.setores:
            if(data.setor == x.nome):
                c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                c.connect(x.ip, self.PORT)
                c.sendall("X")
                c.sendall(self.lixeiras)
                c.close()


class Lixeira:
    travada = False
    capacidade = 0
    ocupacao = 0
    localizacao = ""
    setor = ""

    def __init__(self, localizacao, capacidade, ocupacao):
        self.capacidade = capacidade
        self.ocupacao = ocupacao
        self.localizacao = localizacao
        pass

if __name__ == "__main__":
    
    nome = input("Digite o nome do setor: \n")
    setor = Setor(nome)

    def on_connect(client, userdata, flags, rc):
        print("Conectou MQTT")
        client.subscribe(setor.name + "/#", 1)
    

    def on_message(client, userdata, message):
        info = ""
        msg = message.payload
        msg = msg.decode()
        info = msg.split(" ")
        lixeira = Lixeira(info[0], info[1], info[2])
        lixeira.localizacao
        if setor.addLixeira(lixeira) != 1:
            setor.gerenciaLixo(setor.lixeiras, 1, lixeira)
            setor.lixeiras.sort(key=lambda x: x.ocupacao,  reverse= True)
            if len(setor.lixeiras) > 2:
                #Lixeira(100, 50) Lixeira(100, 45) Lixeira(80, 40)
                if setor.lixeiras(2).ocupacao >= setor.lixeiras(2).capacacidade/2:
                    setor.sendLixeiras()
        setor.writeJson()

   
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("mqtt", password="2314")
    client.connect("localhost")
    client.loop_forever()
    while(True):     
       setor.esvazia()
       sleep(1)
