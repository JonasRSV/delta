import flask
import delta.database
from delta.config import config
import json
import sys
import datetime

DB = delta.database.Connection(config)
DB.connect()

class Generic(object):
    def parse_response(cell):
        return {  "id"     : cell[0]
               , "date"    : str(cell[1])
               , "title"   : cell[2]
               , "document": json.loads(str(cell[3]))
               , "type"    : cell[4]
               }

class Motion(object):
    identifier = "mot"

    def parse_response(cell):
        """
        0: ID from Document
        1: Date from Document
        2: Title from Doucument
        3: Actual Document
        4: Type from Document
        5: ID from Motion
        6: Summary from Motion
        7: Party Affiliation Motion
        """
        return {  "id"     : cell[0]
               , "date"    : str(cell[1])
               , "title"   : cell[2]
               , "document": json.loads(str(cell[3]))
               , "type"    : cell[4]
               , "summary" : cell[6]
               , "party"   : cell[7]
               }

class Document(object):
    """Document request object."""
    identifier = "document"

    def __init__(self, id, type, date, limit):
        self.id    = id
        self.type  = type
        self.date  = date
        self.limit = limit

        self.payload = None
        self.sz = None
        self.json = None

        self.handlers = { Motion.identifier: Motion.parse_response }

    def set_payload(self, payload):
        self.payload = payload
        self.sz = len(payload)

        return self

    def parse_response(self, cell):
        if self.type in self.handlers:
            return self.handlers[self.type](cell)
        else:
            return Generic.parse_response(cell)

    def jsonify(self):
        try:
            self.json = json.dumps({n: self.parse_response(response) for n, response
                                   in zip(range(self.sz), self.payload)})
        except Exception as e:
            """Add error handling."""
            print("Failed to parse json {}".format(str(e)))
            sys.exit(1)

        return self.json

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

