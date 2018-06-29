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
        response = { "success": False, "expired": None, "post": None }
        return flask.Response(response, status=500, mimetype="application/json")

    token, expired = config.decode_token(session_token)

    if expired:
        response = { "success": False, "expired": expired, "post": post_information }
        return flask.Response(response, status=500, mimetype="application/json")

    response = { "success": True, "expired": expired, "post": post_information }
    return flask.Response(response, status=200, mimetype="application/json")


@content.route("/posts/", defaults={"path": "main"})
@content.route("/posts/<path:path>", methods=["GET"])
def get_post(path):
    return flask.Response("Here you go posts from {}".format(path), status=200)


@content.route("/like", methods=["POST"])
def like():
    session_token   = None
    like_request    = None
    try:
        request_data = flask.request_data().decode("utf-8")
        request_data = json.loads(request_data)

        session_token = request_data["token"]
        like_request  = request_data["like"]
    except Exception as e:
        config.write_server_log("Unable to parse like request: {}".format(str(e)))
        return flask.Response("Malformed like body", status=500)

    return flask.Response("Totally like that stuff", status=200)

@content.route("/comment", methods=["POST"])
def comment():
    session_token   = None
    comment_request = None
    try:
        request_data = flask.request_data().decode("utf-8")
        request_data = json.loads(request_data)

        session_token    = request_data["token"]
        comment_request  = request_data["comment"]
    except Exception as e:
        config.write_server_log("Unable to parse comment request: {}".format(str(e)))
        return flask.Response("Malformed comment body", status=500)

    return flask.Response("Wow such comment", status=200)


@content.route("/annotate", methods=["POST"])
def annotate():
    session_token   = None
    annotate_request = None
    try:
        request_data = flask.request_data().decode("utf-8")
        request_data = json.loads(request_data)

        session_token = request_data["token"]
        annotate_request  = request_data["annotation"]
    except Exception as e:
        config.write_server_log("Unable to parse annotation request: {}".format(str(e)))
        return flask.Response("Malformed annotation body", status=500)

    return flask.Response("Wow such Annotation", status=200)

