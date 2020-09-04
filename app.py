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
from functools import wraps
from flask import g, request, redirect, url_for
import MySQLdb
from inittables import InitTables
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from model.school_model import School, Faculty, Department, Program, Level

from message_model import group_conv_init, group_conv_mem, personal_conv_init, personal_conv_mem, personal_message_model, group_message_model 
from entertainment_model import news_model, blogger_model, featured_image_model


# Retrieves database configuration from environment variables
mysql_host = os.environ.get('MYSQL_HOST')
mysql_user = os.environ.get('MYSQL_USER')
mysql_password = os.environ.get('MYSQL_PASSWORD')
db_name = os.environ.get('DB_NAME')


# App flask Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + mysql_user + ':' + mysql_password + '@' + mysql_host + '/' + db_name
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')  #The Jwt_secret_key is obtained from environment variables

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
base.Base.metadata.create_all(db.engine, checkfirst=True)

 # This part of the code is to check if the important tables (School, Faculty, Department, Program, Level) have been initialized
Session = sessionmaker(db.engine) 
Session.configure()
session = Session()
if session.query(School).count() == 0 or session.query(Faculty).count() == 0 or session.query(Department).count() == 0 or session.query(Program).count() == 0 or session.query(Level).count() == 0 :
    InitTables(session)

controller = user_controller.UserController(db)     #Create instance of controller to perform some operations

CORS(app)

# Sets up the funtion for checking if a user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'csrf_access_token' not in request.cookies:
            return {'Error': 'You have to login first'}
        return f(*args, **kwargs)
    return decorated_function


# Register a user - either a student, lecturer or mentor
@app.route('/users/register', methods = ['POST'])
def register ():
    try:
        # Gets all input data from the user
        user_name = request.form.get('user_name')
        surname = request.form.get('surname')
        first_name = request.form.get('first_name')
        email = request.form.get('email')
        password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        user_type = request.form.get('user_type')

        getemail = controller.get_email(email)  # Checks to see if the entry email is in the database. If not, it returns None

    except:
        return {'Error': 'Unable to retrieve user details'}


    if str(user_type) == 'Student':
        try:  
            # Gets additional input for a student
            program_id = request.form.get('program_id')
            matric_no = request.form.get('matric_no')
            level_id = request.form.get('level_id')

            if getemail == None:   # If email is not already registered, input the data into the database
                controller.add_data(student_model.Student(
                    user_name, surname, first_name, email, password, user_type, program_id, matric_no, level_id))

                return {'success': 'succesfully updated in the database'}

            elif email == getemail[0]: # If email is already used, notify the user
                return {'Error': 'This email has already been used to register'}
        
        except:  # To notify if a student hasn't conformed to an acceptable input format.
            return {'Error': 'Unable to retrieve student details. Ensure the inputs are valid'}


    elif str(user_type) == 'Lecturer':
        try: 
            # Get additional inpuuts for lecturers
            department_id = request.form.get('department_id')
            title = request.form.get('title')
            position = request.form.get('position')

            if getemail == None:  # If email is not already registered, input the data into the database
                controller.add_data(lecturer_model.Lecturer(
                    user_name, surname, first_name, email, password, user_type, department_id, title, position))

                return {'success': 'succesfully updated in the database'}

            elif email == getemail[0]:   # If email is already used, notify the user
                return {'Error':'This email has already been used to register'}

        except:  # To notify if a lecturer hasn't conformed to an acceptable input format.
            return {'Error': "Unable to save lecturer details. Ensure that the inputs are correct"}
        
  

    elif str(user_type) == 'Mentor':
        try:
            # Gets addional input data for a mentor
            profession = request.form.get('profession')
            company = request.form.get('company')
            title = request.form.get('title')

            if getemail == None:   # If email is not already registered, input the data into the database
                controller.add_data(mentor_model.Mentor(
                    user_name, surname, first_name, email, password, user_type, profession, company, title))

                return {'success': 'succesfully updated in the database'}

            elif email == getemail[0]:    # If email is already used, notify the user
                return {'Error': 'This email has already been used to register'}
 
        except:   # To notify if a mentor hasn't conformed to an acceptable input format.
            return {'Error': 'Unable to get mentor details. Ensure that the inputs are correct'}


    else:        # To notify if a user hasn't conformed to an acceptable input format.
        return {'Error': 'Unable to get user details. Ensure that the inputs are correct'}


# Function to retrieve a user details based on id
@app.route('/users/<id>', methods=['GET'])
@login_required
def get_user(id):
    try:
        resp = controller.get_user(id)   #Gets the details of a user given the user id.
        return resp.to_dict()
    except:
        return {'Error': 'User not found'}



# Function to login
@app.route('/token/auth', methods=['POST'])
def login():
    # Gets email and password inputed by the user
    email = request.form.get('email')
    pass_word = request.form.get('password')
    
    
    try:
        password = controller.get_password(email) # Checks if email has been registered. If this line fails, it runs the except block
        if bcrypt.check_password_hash(password[0], pass_word):    # Checks if password is correct
            user_name = controller.get_user_name(email)

            access_token = create_access_token(identity = {'User name': user_name[0]})
            refresh_token = create_refresh_token(identity = {'User name': user_name[0]})
        
            resp = jsonify({'refresh': True, 'user name': user_name[0]})
            set_access_cookies(resp, access_token)
            return resp, 200
        else:
            return jsonify({'login': False}), 401
    except:
        return jsonify({'login': False}), 401


if __name__ == '__main__':
    app.run(debug=True)
