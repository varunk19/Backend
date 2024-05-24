from flask import Blueprint, request, session
from flask import current_app as app

from models import db, User, Flight

api = Blueprint("api", __name__)


@api.route("/flight-plan", methods=["POST"])
def create_flight_plan():
    user_id = session.get("user-id")
    flight_plan = request.json.get("flight-plan", None)

    if not user_id:
        return {"message": "Not authorised"}, 401
    
    if not flight_plan:
        return {"message": "Invalid input."}, 204

    plan = Flight(userid=user_id, plan=flight_plan)
    db.session.add(plan)
    db.session.commit()

    return {"message": "Request successful"}, 201
