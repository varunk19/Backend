from tests.__init__ import app, client, runner, pilot, pilot_session


def test_create_unauthorised(app, client):
    response = client.post("/flight-plan", json={"plan": "[]"})
    assert response.status_code == 401


def test_create_invalid_flight(app, client, pilot_session):
    response = client.post("/flight-plan", json={"flight-plan": None})
    assert response.status_code == 204


def test_create_valid_flight(app, client, pilot_session):
    response = client.post("/flight-plan", json={"flight-plan": str([[12, 34], [45, 56]])})
    assert response.status_code == 201

