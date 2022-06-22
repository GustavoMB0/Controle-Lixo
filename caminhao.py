import json
from time import sleep
from types import SimpleNamespace
import asyncio
import requests


class caminhao():
    ip = "" 
    lixeiras = []

    def __init__(self, ip):
        
        self.ip = ip
        print("Caminhao inicializado")
    
    def exibir(self):
        print("Lixeiras: \n")
        for j in range(0, self.lixeiras.__len__()):
            lixeira = self.lixeiras[j]
            print(lixeira['setor'] + " " + lixeira['localizacao'] + ":  " + str(lixeira['ocupacao']) + "\n")

    #Criar rota de caminhao
    def readJson(self):
        resposta = requests.get("http://" + self.ip + ":1234/caminhao")
        self.lixeiras = resposta.json()
    
    #Criar rota de caminhao
    def esvaziar(self):
        lixeira = []
        if self.lixeiras.__len__() <= 1:
            return 0
        sleep(5)
        lixeira = self.lixeiras.pop(0)
        lixeira['ocupacao'] = 0
        print(lixeira)
        resposta = requests.post("http://" + self.ip + ":1234" + "/esvazia/"+ lixeira['setor'] , json=lixeira)
        return resposta.status_code

if __name__ == '__main__':
    ip = input("Digite o ip: \n")
    caminhao = caminhao(ip)
    
    while(True):
        caminhao.readJson()
        caminhao.exibir()
        caminhao.esvaziar()

    
        

