from random import random
from time import sleep
import paho.mqtt.client as mqtt
import random

client = mqtt.Client()
client.username_pw_set("mqtt", password="2314")




class Lixeira(object):
    capacidade = 0
    ocupacao = 0
    localizacao = ''
    mqttip = ''
    
    def __init__(self, capacidade, localizacao, mqttip):
        self.localizacao = localizacao
        self.capacidade = capacidade
        client.connect(mqttip)#ANCHOR mandar ip do setor via socket
        client.loop_start()
        client.subscribe(mqttip+"/"+ localizacao)
        self.mqttip = mqttip




    def changeState(self):
        client.publish("/" + self.localizacao,("{} {} {}".format(self.localizacao, self.capacidade, self.ocupacao)))
    
    #Metodo para encher a lixeira aleatoriamente com o tempo, Testar tempo para encher e se o espaço dado entre os valores é suficiente
    def encher(self):
        value = random.randint(0, 100000000)
        if value >= 500 and value <= 600:
            if self.ocupacao < self.capacidade:
                self.ocupacao += 10
                self.changeState()
def main():
    def on_message(client, userdata, msg):
        mensagem = msg.payload
        mensagem = mensagem.decode()
        if mensagem == "E":
            lixeira.ocupacao = 0
    
    def on_connect(client, userdata, msg):
        print("Conectou mqtt")
    
    client.on_conenct = on_connect
    client.on_message = on_message
    capacidade = int(input("Digite a capacidade da lixeira \n"))
    rua = input("Digite a rua da lixeira \n")
    mqtt = input("Insira o ip do setor\n")

    lixeira = Lixeira(capacidade, rua, mqtt)
    while(True):
        lixeira.encher()

if __name__ == "__main__":
    main()

    

  