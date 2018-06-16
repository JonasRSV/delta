import flask
import delta.database.connection as connection
import delta.database.connection as connection
from delta.config import config
from delta.api.document import Document
import sys
import datetime


DB = connection.Connection(config)
document_bp = flask.Blueprint("Document handler", __name__)

@document_bp.route("/documents", methods=["GET"])
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

    request  = connection.Request(type, Document(id, type, date, limit))
    response = DB.request(request)

    return flask.Response(response.jsonify(), status=200)

