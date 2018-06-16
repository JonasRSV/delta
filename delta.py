import flask
from delta.document_bp import document_bp
from delta.logs_bp     import logs_bp


app = flask.Flask(__name__)
app.register_blueprint(document_bp)
app.register_blueprint(logs_bp)


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

