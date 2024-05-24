from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    userid = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


class Flight(db.Model):
    __tablename__ = "flight"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.ForeignKey("user.id"), nullable=False)
    plan = db.Column(db.String(), nullable=False)
