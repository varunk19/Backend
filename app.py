import sys

# add your project directory to the sys.path
project_home = '/home/varunj6v1k9/mysite'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path
from flask import Flask, jsonify, request
from flask_cors import CORS
import os


def create_app():
    from models import db, User
    from api import api

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL", "sqlite:///project.sqlite")
    app.config["SECRET_KEY"] = "sifeonseurbgld"

    db.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()
        if User.query.filter_by(userid="IA1001").first() is None:
            user = User(userid="IA1001", password="IA0011")
            db.session.add(user)
            db.session.commit()

    app.register_blueprint(api)

    return app


app = create_app()


if __name__ == "__main__":
    app.run()
