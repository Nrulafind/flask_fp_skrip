from flask import Flask, request
from flask import json

app = Flask(__name__)

class ResponseHandler:
    @staticmethod
    def success_response(message, **kwargs):
        data = {"Message": message, **kwargs}
        return app.response_class(
            response=json.dumps(data),
            status = 200,
            mimetype = 'application/json'
        )
    @staticmethod
    def error_response(message, status_code,**kwargs):
        data = {"Error:": message, **kwargs}
        return app.response_class(
            response=json.dumps(data),
            status = status_code,
            mimetype = 'application/json'
        )