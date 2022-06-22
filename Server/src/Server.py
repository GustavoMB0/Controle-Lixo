from flask import Flask
from flask_restful import Api

class ServerApi():

    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['JSON_AS_ASCII']= False
        self.app.port = 1234

        self.api = Api(self.app)
    def run(self,):
        self.app.run(host = '0.0.0.0', port= 1234, debug = False
        )

serverApi = ServerApi()