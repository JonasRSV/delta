import flask
from delta.content import content


app = flask.Flask(__name__)
app.register_blueprint(content)


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)

