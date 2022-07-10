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

    HOST = "127.0.0.1"
    SERVER = ""
    PORT = "30" #Definir porta para conexão
    myip = "localhost"
    ip = "localhost"
    name = ""
    ocupado = False
    message = ""
    lixeiras = []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, name):
        self.name = name
        self.sendMQtt()
        self.s.bind(self.HOST, self.PORT)
        threading.Thread(target= self.listen, args=(self.s)).start()

    def sendMQtt(self):
        message = {"nome" : self.name, "ip" : self.myip}
        print(message)

    #Metodo para conectar e se comunicar com os outros setores
    def connect(self):
        self.c.connect()

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
            elif re.search("^L[0-9]+$", data):
                nLixeira = int(data.split("L"))
                conn.sendall(self.getLixeira(nLixeira))

    def getLixeira(self, nLixeira):
        listLixeira = []
        if nLixeira <= self.lixeiras.count():
            self.lixeiras.sort(key=lambda x: x.ocupacao,  reverse= True)
            for i in range (0, nLixeira):
                listLixeira.append(self.lixeiras[i])
        #ANCHOR Tratar quando o setor não tiver o numero de lixeiras necessario    



            
        return json.dumps(listLixeira, default=lambda o: o.__dict__)


            
                



                


    def writeJson(self):
        with open("test.json", "w") as out:
            json.dump(self.lixeiras, out, default=lambda o: o.__dict__)
    

    def addLixeira(self, Lixeira):
        if sum(map(lambda x: x.localizacao == Lixeira.localizacao, self.lixeiras)) == 0:
            self.lixeiras.append(Lixeira)
            self.lixeiras.sort(key=lambda x: x.ocupacao,  reverse= True)
            return 1
        else:
            return -1

    def esvazia(self):
       resposta = requests("http://" + self.ip + ":1234/setor/" + self.name)
    



    

class Lixeira:
    capacidade = 0
    ocupacao = 0
    localizacao = ""

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
            for x in setor.lixeiras:
                if lixeira.localizacao == x.localizacao:
                    x.ocupacao = lixeira.ocupacao
            setor.lixeiras.sort(key=lambda x: x.ocupacao,  reverse= True)
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
