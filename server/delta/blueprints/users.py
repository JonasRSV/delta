import flask
import json
import config 
import delta.db.connection as connection

DB = connection.Connection("Users")
users = flask.Blueprint("User blueprint", __name__)

@users.route("/profile/login", methods=["POST"])
def login():
    user     = None
    password = None
    try:
        login_information = flask.request.get_data().decode("utf-8")
        login_information = json.loads(login_information)

        user     = login_information["user"]
        password = login_information["password"]
    except Exception as e:
        config.write_server_log("Unable to parse login request: {}".format(str(e)))
        return flask.Response("Malformed post body", status=500)

    """Login should return session token."""
    return flask.Response(str(hash("SESSION TOKEN")), status=200)


@users.route("/profile/logout", methods=["POST"])
def logout():
    session_token = None
    try:
        session_token = flask.request.get_data().decode("utf-8")
        session_token = json.loads(session_token)
        session_token = session_token["token"]
    except Exception as e:
        config.write_server_log("Unable to parse logout request: {}".format(str(e)))
        return flask.Response("Malformed post body", status=500)

    return flask.Response("Totally removed session token.", status=200)


