import flask
import json
import config 
import delta.db.connection as connection

DB = connection.Connection("Users")
users = flask.Blueprint("User blueprint", __name__)

LOGIN        = "SELECT ID FROM USERS WHERE USERS.NAME = %s AND USERS.PW_HASH = %s;"
INSERT_TOKEN = "UPDATE USERS SET TOKEN = %s WHERE USERS.ID = %s;"
CREATE       = "INSERT INTO USERS (NAME, PW_HASH, EMAIL) VALUES (%s, %s, %s);"

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
        config.write_server_log("Unable to parse login request: {}"\
                .format(str(e)))

        response = { "success": False, "token": None, "message": "Malformed request" }
        response = json.dumps(response)
        return flask.Response(response, status=500, mimetype="application/json")


    password_hash  = config.sign_password(password)

    token = None
    query = connection.Request("login", LOGIN, (user, password_hash), fetcher=lambda c:c.fetchone())

    try:
        user_id  = DB.request(query).data[0]
        token    = config.issue_token(user_id)
    except Exception as e:
        config.write_server_log("Unable to login, reason: {}".format(str(e)))

        response = { "success": False, "token": None, "message": "Server Error" }
        response = json.dumps(response)
        return flask.Response(response, status=500, mimetype="application/json")

    query  = connection.Request("update_token", INSERT_TOKEN, (token, user_id))
    try:
        DB.request(query)
    except Exception as e:
        config.write_server_log("Failed to Login, Session Update failed: {}"\
                .format(str(e)))

        response = { "success": False, "token": None, "message": "Server Error" }
        response = json.dumps(response)
        return flask.Response("Login Failed, Server Error", status=500)

    response = { "success": True, "token": token, "message": "Welcome!" }
    response = json.dumps(response)
    return flask.Response(response, status=200, mimetype="application/json")


@users.route("/profile/logout", methods=["POST"])
def logout():
    session_token = None
    try:
        session_token = flask.request.get_data().decode("utf-8")
        session_token = json.loads(session_token)
        session_token = session_token["token"]
    except Exception as e:
        config.write_server_log("Unable to parse logout request: {}".format(str(e)))

        response = { "success": False, "token": None, "message": "Malformed request" }
        response = json.dumps(response)
        return flask.Response(response, status=500, mimetype="application/json")

    user_id = None
    try:
        user_id, expired = config.decode_token(session_token)
    except Exception as e:
        config.write_server_log("Invalid Token, Cannot Log Out: {}".format(str(e)))

        response = { "success": False, "token": token, "message": "Logout Failed" }
        response = json.dumps(response)
        return flask.Response(response, status=500, mimetype="application/json")

    if not expired:
        query = connection.Request("update_token", INSERT_TOKEN, ("None", user_id))

        try:
            DB.request(query)
        except Exception as e:
            config.write_server_log("Failed to Logout, Session Update Failed: {}"\
                    .format(str(e)))

            response = { "success": False, "token": token, "message": "Logout Failed" }
            response = json.dumps(response)
            return flask.Response(response, status=500, mimetype="application/json")
        
    response = { "success": True, "token": None, "message": "Thank you! Come again!" }
    response = json.dumps(response)
    return flask.Response(response, status=200, mimetype="application/json")


@users.route("/profile/create", methods=["POST"])
def create():
    user     = None
    password = None
    email    = None
    try:
        login_information = flask.request.get_data().decode("utf-8")
        login_information = json.loads(login_information)

        user     = login_information["user"]
        password = login_information["password"]
        email    = login_information["email"]
    except Exception as e:
        config.write_server_log("Unable to parse create request: {}".format(str(e)))

        response = { "success": False, "message": "Malformed post body" }
        response = json.dumps(response)
        return flask.Response(response, status=500, mimetype="application/json")

    password_hash  = config.sign_password(password)

    query = connection.Request("create_user", CREATE, (user, password_hash, email))

    try:
        DB.request(query)
    except Exception as e:
        config.write_server_log("Failed to Create User: {}".format(str(e)))

        response = { "success": False, "message": "User with Email already exists" }
        response = json.dumps(response)
        return flask.Response(response, status=500, mimetype="application/json")

    response = { "success": True, "message": "Welcome to the club!" }
    response = json.dumps(response)
    return flask.Response(response, status=200)

