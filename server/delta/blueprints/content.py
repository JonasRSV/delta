import flask
import json
import config 
import delta.db.connection as connection


DB = connection.Connection("Content")
content = flask.Blueprint("Content Blueprint", __name__)

@content.route("/posts/create", methods=["POST"])
def create_post():
    session_token    = None
    post_information = None
    try:
        request_data = flask.request_data().decode("utf-8")
        request_data = json.loads(request_data)

        session_token     = request_data["token"]
        post_information  = request_data["post"]
    except Exception as e:
        config.write_server_log("Unable to parse post request: {}".format(str(e)))
        return flask.Response("Malformed post body", status=500)

    return flask.Response("Totally added post", status=200)


@content.route("/posts/", defaults={"path": "main"})
@content.route("/posts/<path:path>", methods=["GET"])
def get_post(path):
    return flask.Response("Here you go posts from {}".format(path), status=200)

