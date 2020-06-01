import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from flask_wtf.csrf import CSRFProtect
from model import user_model
from model import student_model
from model import lecturer_model
from model import mentor_model

from controller import user_controller
import json
from model import base


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Abayomi1996$@localhost/instucomdb'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
base.Base.metadata.create_all(db.engine, checkfirst=True)

controller = user_controller.UserController(db)

CORS(app)


@app.route('/users/register', methods = ['POST'])
def register ():
    try:
        user_name = request.form.get('user_name')
        surname = request.form.get('surname')
        first_name = request.form.get('first_name')
        email = request.form.get('email')
        password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        user_type = request.form.get('user_type')

    except:
        return {'Error': 'Unable to retrieve user details'}


    if str(user_type) == 'Student':
        try:  
            program_id = request.form.get('program_id')
            matric_no = request.form.get('matric_no')
            level_id = request.form.get('level_id')

            if email != controller.get_email(email):
                controller.add_data(student_model.Student(
                    user_name, surname, first_name, email, password, user_type, program_id, matric_no, level_id))
                
            else:
                
                return {'Error': 'This email has already been used to register'}
        
        except:
            return {'Error': 'Unable to retrieve student details'}

    elif str(user_type) == 'Lecturer':
        try: 
            department_id=request.form.get('department_id')
            title = request.form.get('title')
            position = request.form.get('position')

            if email != controller.get_email(email):
                controller.add_data(lecturer_model.Lecturer(
                    user_name, surname, first_name, email, password, user_type, department_id, title, position))

            else:

                return {'Error': 'This email has already been used to register'}
            
  
        except:
            return {'Error': 'Unable to retrieve lecturer details'}
    

    elif str(user_type) == 'Mentor':
        try:
            profession = request.form.get('profession')
            company = request.form.get('company')
            title = request.form.get('title')

            if email != controller.get_email(email):
                controller.add_data(mentor_model.Mentor(
                    user_name, surname, first_name, email, password, user_type, profession, company, title))

            else:
                return {'Error': 'This email has already been used to register'}
            
 
        except:
            return {'Error': 'Unable to retrieve mentor details'}

    result = jsonify({'success':'succesfully updated in the database'})
    return result


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    resp = controller.get_user(id)
    return resp.to_dict()


@app.route('/token/auth', methods=['POST'])
def login():

    email = request.form.get('email')
    pass_word = request.form.get('password')

    if bcrypt.check_password_hash(controller.get_password(email), pass_word):
        user_name = controller.get_user_name(email)

        access_token = create_access_token(identity = {'User name': user_name})
        refresh_token = create_refresh_token(identity = {'User name': user_name})
        
        resp = jsonify({'refresh': True, 'user name': user_name})
        set_access_cookies(resp, access_token)
        return resp, 200

    else:
        return jsonify({'login': False}), 401

if __name__ == '__main__':
    app.run(debug=True)
