import os
import sys
import logging
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

sys.path.insert(1, os.path.join(os.path.abspath('.'), 'lib'))

import json
from flask import Flask, request
from flask.ext.restful import Api, Resource, abort
from models import MessageModel


app = Flask(__name__)
api = Api(app)


class Message(Resource):
    def get(self):
        message_id = request.values.get('id', None)
        if message_id is None:
            abort(400, message="Bad Request. Message 'id' was not provided.")
        message = MessageModel.get_by_id(int(message_id))
        if message is None:
            abort(404, message="Message '%s' was not found." % message_id)
        return {'message': message.to_dict()}

    def delete(self):
        message_id = request.values.get('id', None)
        if message_id is None:
            abort(400, message="Please provide a message id.")
        try:
            id = int(message_id)
            messages = MessageModel.get_by_id(id)
        except ValueError:
            if message_id == 'all':
                messages = MessageModel.query().fetch(500)
            else:
                abort(400, message="Id should be a number.")
        if messages is None:
            abort(404, message="Message '%s' was not found." % message_id)

        if type(messages) is list:
            for message in messages:
                message.key.delete()
        else:
            messages.key.delete()
        return {'message': "Message '%s' was deleted successfully." % message_id}

    def post(self):
        ip = request.remote_addr
        name = request.values.get('name', None)
        city = request.values.get('city', None)
        email = request.values.get('email', None)
        message = request.values.get('message', None)
        new_message = MessageModel(
            ip=ip,
            name=name,
            city=city,
            email=email,
            message=message
        )
        try:
            new_message.put()
        except CapabilityDisabledError:
            logging.error(u'App Engine Datastore is currently in read-only mode.')
            abort(500)
        return {'id': new_message.key.id()}, 200, {'Access-Control-Allow-Origin': '*'}


class MessageList(Resource):
    def get(self):
        max = 500
        query = MessageModel.query().order(-MessageModel.date)
        messages = query.fetch(max)
        aaData = []
        for message in messages:
            aaData.append({
                "ip": message.ip,
                "date": message.date.isoformat(),
                "name": message.name,
                "city": message.city,
                "message": message.message,
                "email": message.email,
                "id": message.key.id()
            })
        return {'aaData': aaData}


class Warmup(Resource):
    def get(self):
        return ''

api.add_resource(Message, '/message')
api.add_resource(MessageList, '/message/list')
api.add_resource(Warmup, '/_ah/warmup')

if __name__ == '__main__':
    app.run(debug=True)