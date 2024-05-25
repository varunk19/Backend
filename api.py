import sys

# add your project directory to the sys.path
project_home = '/home/varunj6v1k9/mysite'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path
from flask import Blueprint, request, session, jsonify
from flask import current_app as app
from flask_cors import cross_origin

import re
import random
from json import loads

from models import db, User, Flight
from utils import find_optimal_path

api = Blueprint("api", __name__)


def check(data):
    Id_length = 6
    Password_length = 6
    Id_alphabets_length = 2
    Id_numbers_length = 4

    Id = data["Id"]
    Password = data["Password"]
    if len(Id) != Id_length:
        return 0
    elif len(Password) != Password_length:
        return 0

    alph = re.findall(r"[a-zA-Z]+", Id)
    numb = re.findall(r"[0-9]+", Id)
    pas = re.findall(r"[0-9a-zA-Z]+", Password)

    alphabets = ""
    numbers = ""
    passw = ""

    for x in alph:
        alphabets += x
    for x in numb:
        numbers += x
    for x in pas:
        passw += x

    if len(alphabets) + len(numbers) != Id_length:
        return 0
    if len(alphabets) != Id_alphabets_length:
        return 0
    if len(numbers) != Id_numbers_length:
        return 0

    if alphabets != Id[0:2] or numbers != Id[2:6]:
        return 0
    if len(passw) != Password_length:
        return 0

    return 1


@api.route('/login', methods=['POST'])
def Login():
    data = request.get_json()

    ID, PASSWORD = data.get("user-id", ""), data.get("password", "")

    valid = check({"Id": ID, "Password": PASSWORD})

    if not valid:
        return jsonify("Invalid username or password"), 404

    valid_user = User.query.filter_by(userid=ID, password=PASSWORD).first()

    if valid_user:
        session["user-id"] = valid_user.id
        session.modified = True
        return jsonify("Login successful.")
    else:
        return jsonify("User not found."), 404


@api.route("/flight-plan", methods=["POST"])
def create_flight_plan():
    user_id = request.json.get("flight_id")
    flight_plan = request.json.get("flight-plan", None)

    # print(user_id)
    # if not user_id:
    #     return {"message": "Not authorised"}, 401

    if not flight_plan:
        return {"message": "Invalid input."}, 204

    plan = Flight(user_id=user_id, plan=flight_plan)
    db.session.add(plan)
    db.session.commit()

    return {"plan-id": plan.id}, 201


@api.route("/flight-plan/<int:plan_id>", methods=["POST"])
def edit_flight_plan(plan_id):
    plan = db.session.query(Flight).get(plan_id)
    flight_plan = request.json.get("flight-plan", None)

    if not plan:
        return {"message": "Flight plan not found"}, 404

    if session.get("user-id") or plan.user_id != session.get("user-id"):
        return {"message": "Not authorised"}, 401

    if not flight_plan:
        return {"message": "Invalid input."}, 204

    plan.plan = flight_plan
    db.session.commit()

    return {"message": "Request sucessfull"}


@api.route("/fetch_flight-plan", methods=["POST"])
def fetch_flight_plan():
    data=request.get_json()
    
    user_id = data.get('user_id',"")
    flight_plan = Flight.query.filter_by(user_id=user_id).first()

    if not flight_plan:
        return {"message": "There is no flight plan with this id."}, 200
    else:
        return loads(flight_plan.plan), 200


@api.route("/find_best_route", methods=["POST"])
def find_best_route():
    data = request.get_json()
    flight_source, flight_destination, excluded_airport, included_airport = (
        data.get("source", ""),
        data.get("destination", ""),
        data.get("excluded_airport", ""),
        data.get("included_airport", ""),
    )
    if not flight_source or not flight_destination:
        return {"message": "Invalid flight plan."}, 404

    result = find_optimal_path(
        flight_destination=flight_destination,
        flight_source=flight_source,
        excluded_airport=excluded_airport,
        included_airport=included_airport,
    )
    return jsonify(result)


@api.route("/flight-plan/<int:plan_id>/status", methods=["POST"])
def flight_plan_alert(plan_id):
    plan = db.session.query(Flight).get(plan_id)

    if plan is None:
        return {"message": "Flight plan not found."}, 404

    source = request.json.get("source")
    destination = request.json.get("destination")
    excluded = request.json.get("excluded-airport", "")
    included = request.json.get("included-airport")

    
    route = random.choice(
        find_optimal_path(source, destination, excluded, included)
    )

    return {
        "alert": "There is a storm in the path",
        "route": route,
    }


