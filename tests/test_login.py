from tests.__init__ import app, client, runner


def test_empty_login(app, client):
    assert client.post("/login", json={}).status_code == 404


def test_invalid_login(app, client):
    assert client.post("/login", json={"user-id": "foo", "password": "bar"}).status_code == 404


