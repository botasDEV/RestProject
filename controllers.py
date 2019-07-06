import models
from flask_restful import Resource


class ClientController(Resource):
    @staticmethod
    def root():
        return {"ola": "mundo"}

