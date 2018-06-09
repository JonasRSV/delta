import flask
from delta.connection import Connection
from delta.config import config
from delta.request.document import Document
import sys
import datetime


DB = Connection(config)
DB.connect()


class Request(object):

    def __init__(self, type, data):
        self.type = type
        self.data = data

    def set_type(self, type):
        self.type = type
        return self

    def set_data(self, data):
        self.data = data
        return self

content = flask.Blueprint("Content handler", __name__)


@content.route("/content/documents", methods=["GET"])
def get_documents():
    """Get returns None and does not throw exception if param is missing"""
    id    = flask.request.args.get("id")
    type  = flask.request.args.get("type")
    date  = flask.request.args.get("date")
    limit = flask.request.args.get("limit")

    if date is None:
        date = datetime.datetime.today().strftime('%Y-%m-%d')

    if type is None:
        type = Document.identifier

    request  = Request(type, Document(id, type, date, limit))
    response = DB.request(request)

    return flask.Response(response.jsonify(), status=200)

