from tests.__init__ import app, client, runner, pilot, pilot_session
from models import db, Flight


def test_create_unauthorised(app, client):
    response = client.post("/flight-plan", json={"plan": "[]"})
    assert response.status_code == 401


def test_create_invalid_flight(app, client, pilot_session):
    response = client.post("/flight-plan", json={"flight-plan": None})
    assert response.status_code == 204


def test_create_valid_flight(app, client, pilot_session):
    response = client.post("/flight-plan", json={"flight-plan": str([[12, 34], [45, 56]])})
    assert response.status_code == 201


def test_edit_flight_plan_logged_out_user(app, client, pilot):
    with app.app_context():
        flight = Flight.query.filter_by(user_id=pilot.id).first()

    response = client.post(f"/flight-plan/{flight.id}", json={"flight-plan": str([[12, 34], [45, 56]])})

    assert response.status_code == 401


def test_edit_nonexist_flight_plan(app, client, pilot, pilot_session):
    with app.app_context():
        flight = Flight.query.filter_by(user_id=pilot.id)

    response = client.post(f"/flight-plan/{10**6}", json={"flight-plan": str([[12, 34], [45, 56]])})

    assert response.status_code == 404

