import pytest
from app import create_app
from models import db, User


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:////"})

    with app.app_context():
        db.create_all()

        if not User.query.filter_by(userid="im1234").first():
            user = User(userid="im1234", password="123456")
            db.session.add(user)
            db.session.commit()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def pilot(app):
    with app.app_context():
        user = User.query.filter_by(userid="im1234").first()
    return user


@pytest.fixture()
def pilot_session(app, client, pilot):
    response = client.post(
        "/login", json={"user-id": pilot.userid, "password": pilot.password}
    )
    assert response.status_code == 200

    return True
