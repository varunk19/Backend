from flask import Flask,jsonify,request


def create_app():
    from models import db
    from api import api

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.sqlite"
    app.config["SECRET_KEY"] = "sifeonseurbgld"

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(api)
    
    return app


app = create_app()


if __name__ == "__main__":
    app.run()