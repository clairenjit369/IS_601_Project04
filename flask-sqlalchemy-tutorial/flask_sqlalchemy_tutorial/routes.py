"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, instance_relative_config=False)
app.config.from_object("config.Config")


db = SQLAlchemy()
db.init_app(app)
db.create_all()  # Create database tables for our data models


@app.route("/", methods=["GET"])
def index():
    return "hello"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)
