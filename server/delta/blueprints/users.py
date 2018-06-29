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
        return flask.Response("Malformed post body", status=500)


    password_hash  = config.sign_password(password)

    token = None
    query = connection.Request("login", LOGIN, (user, password_hash), fetcher=lambda c:c.fetchall())

    try:
        user_id  = DB.request(query).extract_login()
        token    = config.issue_token(user_id)
    except Exception as e:
        config.write_server_log("Unable to login, reason: {}".format(str(e)))
        return flask.Response("Login Failed, Server Error", status=500)

    query  = connection.Request("update_token", INSERT_TOKEN, (token, user_id))
    try:
        DB.request(query)
    except Exception as e:
        config.write_server_log("Failed to Login, Session Update failed: {}"\
                .format(str(e)))
        return flask.Response("Login Failed, Server Error", status=500)

    return flask.Response(token, status=200)


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

    user_id = None
    try:
        user_id, expired = config.decode_token(session_token)
    except Exception as e:
        config.write_server_log("Invalid Token, Cannot Log Out: {}".format(str(e)))
        return flask.Response("Logout Failed", status=500)

    if not expired:
        query = connection.Request("update_token", INSERT_TOKEN, ("None", user_id))

        try:
            DB.request(query)
        except Exception as e:
            config.write_server_log("Failed to Logout, Session Update Failed: {}"\
                    .format(str(e)))
            return flask.Response("Logout Failed, Server Error", status=500)
        
    return flask.Response("Good Bye, Please Come Again.", status=200)


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
        return flask.Response("Malformed post body", status=500)

    password_hash  = config.sign_password(password)

    print(password_hash)
    
    query = connection.Request("create_user", CREATE, (user, password_hash, email))

    try:
        DB.request(query)
    except Exception as e:
        config.write_server_log("Failed to Create User: {}".format(str(e)))
        return flask.Response("User with Email already exists", status=500)

    return flask.Response("Welcome Friend.", status=200)

