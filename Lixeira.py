from random import random
from time import sleep
import paho.mqtt.client as mqtt
import random





class Lixeira(object):
    capacidade = 0
    ocupacao = 0
    localizacao = ''
    
    def __init__(self, capacidade, localizacao, mqtt):
        self.localizacao = localizacao
        self.capacidade = capacidade
        client.connect(mqtt)#ANCHOR mandar ip do setor via socket
        client.loop_start()
        client.subscribe(mqtt+"/"+ localizacao)
   




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
    client = mqtt.Client()
    client.on_message = on_message
    client.username_pw_set("mqtt", password="2314")
    capacidade = int(input("Digite a capacidade da lixeira \n"))
    rua = input("Digite a rua da lixeira \n")
    mqtt = input("Insira o ip do setor\n")

    lixeira = Lixeira(capacidade, rua, mqtt)
    def on_message(client, userdata, msg):
        mensagem = msg.payload
        mensagem = mensagem.decode()
        if mensagem == "E":
            lixeira.ocupacao = 0
    while(True):
        lixeira.encher()

if __name__ == "__main__":
    main()

    

  