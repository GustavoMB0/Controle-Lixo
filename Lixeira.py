from random import random
from time import sleep
import paho.mqtt.client as mqtt
import random


def on_connect(client, userdata, flags, rc):
    print("Conectou MQTT")
    

def on_message(client, userdata, msg):
    print(msg.topic+" -  "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("mqtt", password="2314")

class Lixeira(object):
    capacidade = 0
    ocupacao = 0
    localizacao = ''
    
    def __init__(self, capacidade, localizacao, mqtt):
        self.localizacao = localizacao
        self.capacidade = capacidade
        client.connect(mqtt)#ANCHOR mandar ip do setor via socket
        client.loop_start()




    def changeState(self):
        client.publish(self.mqtt + "/" + self.localizacao,("{} {} {}".format(self.localizacao, self.capacidade, self.ocupacao)))
    
    #Metodo para encher a lixeira aleatoriamente com o tempo, Testar tempo para encher e se o espaço dado entre os valores é suficiente
    def encher(self):
        value = random.randint(0, 100000000)
        if value >= 500 and value <= 600:
            if self.ocupacao < self.capacidade:
                self.ocupacao += 10
                self.changeState()
    
def main():
    capacidade = int(input("Digite a capacidade da lixeira \n"))
    rua = input("Digite a rua da lixeira \n")
    mqtt = input("Insira o ip do setor\n")

    lixeira = Lixeira(capacidade, rua, mqtt)
    while(True):
        lixeira.encher()

if __name__ == "__main__":
    main()
    
    #client.on_connect = on_connect
    #client.on_message = on_message
    #client.username_pw_set("hiago23rangel@gmail.com", password="2314")

    # Conecta no MQTT Broker, no meu caso, o Maquiatto
    #client.connect("www.maqiatto.com", 1883, 60)

    #client.publish("hiago23rangel@gmail.com/luz1", "Oi, aqui é um teste")

    # Inicia o loop
    

  