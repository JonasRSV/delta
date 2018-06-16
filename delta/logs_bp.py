import flask
from delta.config import config


logs_bp = flask.Blueprint("Logs handler", __name__)

@logs_bp.route("/logs/<path:path>", methods=["GET"])
def logs(path):
    response = None
    with open("logs/{}".format(path), "r") as log_file:
        response = flask.Response(log_file.read(), status=200, mimetype="text/plain")

    return response

@logs_bp.route("/logs/", methods=["GET"])
def log_info():
    return flask.Response("visit: /logs/[server.log]", status=200)
