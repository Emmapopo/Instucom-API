from flask import Flask, jsonify, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)


app = Flask(__name__)

app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD'] = 'Abayomi1996$'
app.config['MYSQL_DB'] = 'instucomdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['JWT_SECRET_KEY'] = 'secret'

mysql = MySQL(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)

@app.route('/users/register', methods = ['POST'])
def register ():
    cur = mysql.connection.cursor()
    user_name = request.form.get('user_name')
    surname = request.form.get('surname')
    first_name = request.form.get('first_name')
    email = request.form.get('email')
    password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
    user_type = request.form.get('user_type')

    cur.execute('''INSERT IGNORE INTO user(user_name, surname, first_name, email, password, user_type)
        VALUES (%s,%s,%s,%s,%s,%s)''', (user_name, surname, first_name, email, password, user_type))
    cur.execute("SELECT id FROM user WHERE email = %s ", (email,))
    user_id = cur.fetchone()["id"]

    if str(user_type) == 'Student' or str(user_type) == 'Lecturer':
        department = request.form.get('department')
        faculty = request.form.get('faculty')
        school = request.form.get('school')
        cur.execute("INSERT IGNORE INTO School (school_name) VALUES (%s)", (school,))
        cur.execute("SELECT id FROM School WHERE school_name = %s ", (school,))
        school_id = cur.fetchone()["id"]

        cur.execute("INSERT IGNORE INTO Faculty (faculty, school_id) VALUES (%s, %s)", (faculty,school_id))
        cur.execute("SELECT id FROM Faculty WHERE faculty = %s ", (faculty,))
        faculty_id = cur.fetchone()["id"]

        cur.execute("INSERT IGNORE INTO Department (department, faculty_id) VALUES (%s, %s)",(department,faculty_id))
        cur.execute("SELECT id FROM Department WHERE department = %s ", (department,))
        department_id = cur.fetchone()["id"]


        if str(user_type) == 'Student':
            program = request.form.get('program')
            matric_no = request.form.get('matric_no')
            level = request.form.get('level')

            cur.execute("INSERT IGNORE INTO Program (program, department_id) VALUES (%s, %s)",(program, department_id))
            cur.execute('SELECT id FROM Program WHERE program = %s', (program,))
            program_id = cur.fetchone()["id"]

            cur.execute("INSERT IGNORE INTO Level (level) VALUES (%s)",(level,))
            cur.execute('SELECT id FROM Level WHERE level = %s', (level,))
            level_id = cur.fetchone()["id"]

            cur.execute('''INSERT IGNORE INTO Student (user_id, program_id, matric_no, level_id)
                VALUES (%s, %s, %s, %s)''', (user_id, program_id, matric_no, level_id))

        elif str(user_type) == 'Lecturer':
            title = request.form.get('title')
            position = request.form.get('position')
            cur.execute('''INSERT IGNORE INTO Lecturer (user_id, department_id, title, position)
                VALUES (%s, %s, %s, %s)''', (user_id, department_id, title, position))


    elif str(user_type) == 'Mentor':
        profession = request.form.get('profession')
        company = request.form.get('company')
        title = request.form.get('title')

        cur.execute('''INSERT IGNORE INTO Mentor (user_id, profession, company, title)
            VALUES (%s, %s, %s, %s)''', (user_id, profession, company, title))

    mysql.connection.commit()
    result = jsonify({'success':'succesfully updated in the database'})
    return result

@app.route('/users/login', methods = ['POST'])
def login():
    cur = mysql.connection.cursor()
    email = request.form.get('email')
    password = request.form.get('password')

    cur.execute('SELECT * FROM User WHERE email = %s', (email,))
    rv = cur.fetchone()["password"]

    cur.execute('SELECT * FROM User WHERE  email= %s', (email,))
    user_name = cur.fetchone()["user_name"]

    if bcrypt.check_password_hash(rv, password):
        access_token = create_access_token(identity = {'User name': user_name})
        result = access_token

    else:
        result = jsonify({'error':'Invalid username or password'})

    return result

if __name__ == '__main__':
    app.run(debug=True)
