"""
models.py

App Engine datastore models

"""

from google.appengine.ext import ndb


class MessageModel(ndb.Model):
    """Stream Model"""
    ip = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    name = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    message = ndb.TextProperty(required=True)

    def to_dict(self):
        result = {
            'ip': self.ip,
            'date': self.date.isoformat(),
            'name': self.name,
            'city': self.city,
            'email': self.email,
            'message': self.message
        }
        return result
