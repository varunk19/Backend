from flask import Blueprint, request, session, jsonify
from flask import current_app as app

import re

from models import db, User, Flight
from utils import find_optimal_path

api = Blueprint("api", __name__)


Id_length=6
Password_length=6
Id_alphabets_length=2
Id_numbers_length=4


def check(data):
    Id=data['Id']
    Password=data['Password']
    if len(Id)!=Id_length:
        return f'Id must be of length {Id_length}'
    elif len(Password)!=Password_length:
        return f'Password must be of length {Password_length}'
    
    
    
    alph=re.findall(r'[a-zA-Z]+',Id)
    numb=re.findall(r'[0-9]+',Id)
    pas=re.findall(r'[0-9]+',Password)
    
    alphabets=''
    numbers=''
    passw=''
    
    for x in alph:
        alphabets+=x
    for x in numb:
        numbers+=x
    for x in pas:
        passw+=x
    
    
    if len(alphabets)+len(numbers)!=Id_length:
        return 'Id must consist of only letters and alphabets'
    if len(alphabets)!=Id_alphabets_length:
        return f'Id must include {Id_alphabets_length} alphabets'
    if len(numbers)!=Id_numbers_length:
        return f'Id must include {Id_numbers_length} alphabets'
    
    if alphabets!=Id[0:2] or numbers!=Id[2:6]:
        return 'Id is not in the following pattern AI1000' 
    if len(passw)!=Password_length:
        return 'Password must consist of only numbers'
    
    return 'ok'
    

@api.route('/login', methods=['POST'])
def Login():
    data=request.get_json()

    ID,PASSWORD=data.get('user-id', ""),data.get('password', "")
    
    valid=check({'Id':ID,'Password':PASSWORD})


    if not valid:
        return jsonify("Invalid username or password"), 404
    
    valid_user = User.query.filter_by(userid=ID, password=PASSWORD).first()
    
    if valid_user:
        session["user-id"] = valid_user.id
        return jsonify('Login successful.')
    else:
        return jsonify('User not found.'), 404
    

@api.route("/flight-plan", methods=["POST"])
def create_flight_plan():
    user_id = session.get("user-id")
    flight_plan = request.json.get("flight-plan", None)

    if not user_id:
        return {"message": "Not authorised"}, 401
    
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


@api.route("/flight-plan/<int:plan_id>")
def flight_plan_alert(plan_id):
    return find_optimal_path('AER', 'KZN', "", "")
