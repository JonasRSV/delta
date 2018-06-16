import flask
import json
from delta.config import write_server_log, config
import delta.database.connection as connection


DB = connection.Connection(config, "post")
posts_bp = flask.Blueprint("Post handler", __name__)

@posts_bp.route("/posts/create", methods=["POST"])
def create_post():
    session_token    = None
    post_information = None
    try:
        request_data = flask.request_data().decode("utf-8")
        request_data = json.loads(request_data)

        session_token     = request_data["token"]
        post_information  = request_data["post"]
    except Exception as e:
        write_server_log("Unable to parse post request: {}".format(str(e)))
        return flask.Response("Malformed post body", status=500)

    return flask.Response("Totally added post", status=200)


@posts_bp.route("/posts/", defaults={"path": "main"})
@posts_bp.route("/posts/<path:path>", methods=["GET"])
def get_post(path):
    return flask.Response("Here you go posts from {}".format(path), status=200)

