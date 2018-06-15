import json
from delta.request.motion import Motion
from delta.request.generic import Generic
import sys

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

