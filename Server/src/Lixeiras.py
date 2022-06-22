
import json
from pickle import FALSE
from flask import Flask, request
from flask_restful import Api, Resource
from Server import serverApi

app = serverApi.app
api = serverApi.api
lixo = []
setor = []
lixeiraVazia = []
lixeiraVazia.append( {'setor': 'invalid'})
class Lixeira(Resource):
    
    @app.route("/esvazia/<setor>", methods = ['GET'])
    def getEsvazia(setor):
        if(lixeiraVazia[0]['setor'] == setor ):
            return lixeiraVazia[0]
        else:
           return {}

    @app.route("/esvazia/<setor>", methods = ['POST'])
    def postEsvazia(setor):
        entrada = request.get_json()
        lixeiraVazia[0] ={'setor': setor, 'localizacao': entrada['localizacao'], 'capacidade': entrada['capacidade'], 'ocupacao': entrada['ocupacao']}
        return '1'

    

    @app.route("/lixeira/<setor>", methods =['POST'])
    def getLixeira(setorlixeira):
        entrada = request.get_json()
        for j in range(0, len(entrada)):
            lixeira = entrada[j]
            existe = False
            for i in range(0, len(lixo)):
                cl = lixo[i]
                #if (setorlixeira  == cl['setor']):
                if(lixeira['localizacao'] == cl['localizacao']):
                    cl = {'localizacao': lixeira['localizacao'], 'capacidade': lixeira['capacidade'], 'ocupacao': lixeira['ocupacao']}
                    existe = True
            if(not existe):
                lixo.append( {'localizacao': lixeira['localizacao'], 'capacidade': lixeira['capacidade'], 'ocupacao': lixeira['ocupacao']})
        return "1"
        

    @app.route("/caminhao", methods = ['GET'])
    def caminhaoSaida():
        lixo.sort(key=lambda x: x['ocupacao'],  reverse= True)
        if(len(lixo)>=10):
            saida = []
            for j in range(0, 10):
                saida.append(lixo[j])
            return json.dumps(saida, default= lambda o: o.__dict__)
        else:
            return json.dumps(lixo, default= lambda o: o.__dict__)


    @app.route("/setor/<nome>", methods = ['GET'])
    def getSetor(nome):
        for j in range(0, len(setor)):
            cl = setor[j]
            print(cl)
            if(cl['nome']== nome ):
                return json.dumps(setor[j], default= lambda o: o.__dict__) 
        return '{}'
        
    @app.route("/setor", methods =['POST'])
    def postSetor():
        entrada = request.get_json()
        existe = False
        for j in range(0, len(setor)):
            cl = setor[j]
            if (cl['nome'] == entrada['nome']):
                setor[j] == entrada
        if(not existe):
            setor.append(entrada)
        return "1"

