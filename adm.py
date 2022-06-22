import json
from time import sleep
from types import SimpleNamespace
import asyncio
import requests

class adm():
    lixeiras = []
    ip = "" 
    
    def __init__(self, ip):
        self.ip = ip
        print("Caminhao inicializado")
    
    def exibir(self):
        print("Lixeiras: \n")
        print(self.lixeiras['setor'] + " " + self.lixeiras['localizacao'] + ":  " + self.lixeiras['ocupacao'] + "\n")

    #Criar rota de caminhao
    def readJson(self):
        resposta = requests.get("http://" + self.ip + ":5000/caminhao")
        self.lixeiras = resposta.json

if __name__ == '__main__':
    ip = input("Digite o ip: \n")
    adm = adm(ip)
    
    while(True):
        adm.readJson()
        adm.exibir()