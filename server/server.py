import flask
from delta.blueprints.content  import content
from delta.blueprints.logs     import logs
from delta.blueprints.users    import users

#REMOVE LATER
from flask_cors import CORS

app = flask.Flask(__name__)

app.register_blueprint(content)
app.register_blueprint(logs)
app.register_blueprint(users)

#REMOVE LATER
CORS(app)


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

