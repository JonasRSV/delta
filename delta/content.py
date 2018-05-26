import flask
import delta.database
from delta.config import config
import json
import sys

DB = delta.database.Connection(config)
DB.connect()


class Document(object):
    """Document request object."""

    def __init__(self, id, type, date, limit):
        self.id    = id
        self.type  = type
        self.date  = date
        self.limit = limit

        self.payload = None
        self.sz = None
        self.json = None

    def set_payload(self, payload):
        self.payload = payload
        self.sz = len(payload)

        return self

    def parse_response(self, cell):
        return {  "id":       cell[0]
                , "date":     str(cell[1])
                , "title":    cell[2]
                , "document": cell[3]
               }


    def jsonify(self):
        try:
            self.json = json.dumps({n: self.parse_response(response) for n, response
                                   in zip(range(self.sz), self.payload)})
        except Exception as e:
            """Add error handling."""
            print("Failed to parse json {}".format(str(e)))
            sys.exit(1)

        return self.json




content = flask.Blueprint("Content handler", __name__)


@content.route("/content/documents", methods=["GET"])
def get_documents():
    """Get returns None and does not throw exception if param is missing"""
    id    = flask.request.args.get("id")
    type  = flask.request.args.get("type")
    date  = flask.request.args.get("date")
    limit = flask.request.args.get("limit")

    request  = Document(id, type, date, limit)
    response = DB.request_documents(request)

    return flask.Response(response.jsonify(), status=200)

