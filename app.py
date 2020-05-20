from flask import Flask, jsonify, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)
from controller import app_controller
from model import database
from model import user_model


class App:
    def __init__(self, appController):
        self.app = appController

    def user(self, *s):
        self.app.insert_user(*s)

    def student(self, *s):
        self.app.insert_student(*s)

    def lecturer(self, *s):
        self.app.insert_lecturer(*s)

    def mentor(self, *s):
        self.app.insert_mentor(*s)

    def user_id(self, *s):
        user_id = self.app.fetch_user_id(s)
        return user_id
    
    def program_id(self, *s):
        program_id = self.app.fetch_program_id(s)
        return program_id

    def level_id (self, *s):
        level_id = self.app.fetch_level_id(s)
        return level_id

    def department_id(self, *s):
        department_id = self.app.fetch_department_id(s)
        return department_id

    def password(self,*s):
        password = self.app.fetch_password(s)
        return password

    def username(self,*s):
        username = self.app.fetch_user_name(s)
        return username




app = Flask(__name__)

app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD'] = 'Abayomi1996$'
app.config['MYSQL_DB'] = 'instucomdb'
app.config['JWT_SECRET_KEY'] = 'secret'

mysql = MySQL(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)


@app.route('/users/register', methods = ['POST'])
def register ():
    db = database.Database(mysql)
    appInstance = app_controller.AppController(db)
    A1 = App(appInstance)
    user1 = user_model.UserModel()
    user_name = request.form.get('user_name')
    user1.set_user_name(user_name)

    surname = request.form.get('surname')
    user1.set_surname(surname)

    first_name = request.form.get('first_name')
    user1.set_first_name(first_name)

    email = request.form.get('email')
    user1.set_email(email)

    password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
    user1.set_password(password)

    user_type = request.form.get('user_type')
    user1.set_user_type(user_type)
    

    A1.user([user_name, surname, first_name, email, password, user_type])
    user_id = A1.user_id(email)
    user1.set_user_id(user_id)

    if str(user_type) == 'Student':
        student1 = user_model.StudentModel()
        student1.set_user_id(user_id) 
        
        program = request.form.get('program')
        matric_no = request.form.get('matric_no')
        student1.set_matric_no(matric_no) 

        level = request.form.get('level')
        
        program_id = A1.program_id(program)
        student1.set_program_id(program_id) 
        
        level_id = A1.level_id(level)
        student1.set_level_id(level_id) 

        A1.student([student1.get_user_id(), student1.get_program_id(), student1.get_matric_no(), student1.get_level_id()])

    elif str(user_type) == 'Lecturer':
        lecturer1 = user_model.LecturerModel()
        lecturer1.set_user_id(user_id)

        title = request.form.get('title')
        lecturer1.set_title(title)
        
        position = request.form.get('position')
        lecturer1.set_position(position)

        department = request.form.get('department')
        department_id = A1.department_id(department)
        lecturer1.set_department_id(department_id)

        A1.lecturer([lecturer1.get_user_id(), lecturer1.get_department_id(), lecturer1.get_title(), lecturer1.get_position()])



    elif str(user_type) == 'Mentor':
        mentor1 = user_model.MentorModel()
        mentor1.set_user_id(user_id)

        profession = request.form.get('profession')
        mentor1.set_profession(profession)

        company = request.form.get('company')
        mentor1.set_company(company)

        title = request.form.get('title')
        mentor1.set_title(title)

        A1.mentor([mentor1.get_user_id(), mentor1.get_profession(), mentor1.get_company(), mentor1.get_title()])


    result = jsonify({'success':'succesfully updated in the database'})
    return result


@app.route('/users/login', methods = ['POST'])
def login():
    db = database.Database(mysql)
    appInstance = app_controller.AppController(db)
    A1 = App(appInstance)
    user1 = user_model.UserModel()
    email = request.form.get('email')
    user1.set_email(email)
    
    pass_word = request.form.get('password')
    user1.set_password(pass_word)

    db_password = A1.password(user1.get_email())
    user_name = A1.username(user1.get_email())


    if bcrypt.check_password_hash(db_password, user1.get_password()):
        access_token = create_access_token(identity = {'User name': user_name})
        result = access_token

    else:
        result = jsonify({'error':'Invalid username or password'})

    return result

if __name__ == '__main__':
    app.run(debug=True)
