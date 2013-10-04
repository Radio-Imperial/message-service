import os
import sys

sys.path.insert(1, os.path.join(os.path.abspath('.'), 'lib'))

from flask import Flask
from flask.ext import restful
from models import MessageModel

app = Flask(__name__)
api = restful.Api(app)


class Message(restful.Resource):
    def get(self, message_id):
        return {'hello': 'world'}


class MessageList(restful.Resource):
    def get(self):
        return {
            "aaData": [
                [
                    "10.10.10.10",
                    "1/1/1",
                    "Tester",
                    "Aqui",
                    "Mensagem",
                    "tester@tester",
                    "10",
                ],
                [
                    "10.10.10.10",
                    "1/1/1",
                    "Tester",
                    "Aqui",
                    "Mensagem",
                    "tester@tester",
                    "10",
                ],
                [
                    "10.10.10.10",
                    "1/1/1",
                    "Tester",
                    "Aqui",
                    "Mensagem",
                    "tester@tester",
                    "10",
                ]
            ]
        }


class Warmup(restful.Resource):
    def get(self):
        return ''

api.add_resource(Message, '/message/<string:message_id>')
api.add_resource(MessageList, '/message/list')
api.add_resource(Warmup, '/_ah/warmup')

if __name__ == '__main__':
    app.run(debug=True)