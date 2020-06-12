from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from model.user_model import User
from model.student_model import Student
from model.lecturer_model import Lecturer
from model.mentor_model import Mentor

class UserController():
    db = None
    def __init__(self, db):
        self.db = db

    def add_data(self,me):         # Function to add data to the database
        self.db.session.add(me)
        self.db.session.commit()

    def get_user(self, id):        # Function to retrieve a user from the database
        resp = self.db.session.query(User).filter_by(id=id).one()
        return resp

    def get_password(self, em):    # Function to retrieve the password of a user from the database
        password = self.db.session.query(User).with_entities(User.password).filter_by(email=em).first()
        return password

    def get_email(self, em):       # Function to retrieve the email of a user from the database
        email = self.db.session.query(User).with_entities(User.email).filter_by(email=em).first()
        return email

    def get_user_name(self, em):   # Function to retrieve the user name of a user from the database
        username = self.db.session.query(User).with_entities(User.user_name).filter_by(email=em).first()
        return username

