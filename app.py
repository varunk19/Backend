import os

from flask import Flask



def create_app():
    from models import db
    from api import api

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI", "sqlite:///project.sqlite")
    app.config["PASS-SALT"] = os.environ.get("PASS_SALT", "ieidnvsiaonafison").encode()

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(api)

    return app


app = create_app()


if __name__ == "__main__":
    app.run()