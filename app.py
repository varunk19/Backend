from flask import Flask,jsonify,request
import re


def create_app():
    from models import db
    from api import api

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.sqlite"

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(api)
    
    return app


app = create_app()

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
    

@app.route('/Login', methods=['POST'])
def Login():
    data=request.get_json()
    print(data)
    ID,PASSWORD=data['ID'],data['PASSWORD']
    
    valid=check({'Id':ID,'Password':PASSWORD})
    if valid!='ok':
        return jsonify(valid)
    
    conn=get_db_connection()
    valid_user=conn.execute(f"SELECT * FROM user WHERE user.ID='{ID}' AND user.PASSWORD='{PASSWORD}';").fetchall()
    valid_id=conn.execute(f"SELECT * FROM user WHERE user.ID='{ID}';").fetchall()
    conn.close()
    
    if valid_user:
        return jsonify('User is valid')
    elif valid_id:
        return jsonify('Password is incorrect')
    else:
        return jsonify('ID is incorrect')
    



if __name__ == "__main__":
    app.run()