from concurrent.futures import thread
from pickle import TRUE
from pyclbr import Class
import paho.mqtt.client as mqtt
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


    def listen(self):
        self.s.listen()
        while True:
            conn, addr = self.s.accept()
            conn.settimeout(80)
            threading.Thread(target = self.listenToClient, args=(conn, addr)).start()


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
