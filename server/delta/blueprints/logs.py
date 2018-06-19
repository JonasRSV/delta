import flask
import config


logs = flask.Blueprint("Logs Blueprint", __name__)

@logs.route("/logs/<path:path>", methods=["GET"])
def log(path):
    response = None
    with open("logs/{}".format(path), "r") as log_file:
        response = flask.Response(log_file.read(), status=200, mimetype="text/plain")

    return response

@logs.route("/logs/", methods=["GET"])
def log_info():
    return flask.Response("visit: /logs/[server.log]", status=200)
