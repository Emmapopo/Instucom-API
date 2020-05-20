from model import database
from model import user_model


class AppController():
    def __init__(self,db):
        self.db = db

    def insert_user(self, *s):
        self.db.insert_one('''INSERT IGNORE INTO User(user_name, surname, first_name, email, password, user_type)
        VALUES (%s,%s,%s,%s,%s,%s)''', *s)

    def insert_student(self, *s):
        self.db.insert_one('''INSERT IGNORE INTO Student (user_id, program_id, matric_no, level_id)
                   VALUES (%s, %s, %s, %s)''', *s)

    def insert_lecturer(self, *s):
        self.db.insert_one('''INSERT IGNORE INTO Lecturer (user_id, department_id, title, position)
                VALUES (%s, %s, %s, %s)''', *s)

    def insert_mentor(self, *s):
        self.db.insert_one('''INSERT IGNORE INTO Mentor(user_id, profession, company, title)
            VALUES (%s, %s, %s, %s)''', *s)

    def fetch_user_id(self, s):
        self.db.select_one('SELECT id FROM User WHERE email = %s', s)
        record = self.db.fetch_one()
        return record

    def fetch_program_id(self, s):
        self.db.select_one('SELECT id FROM Program WHERE program = %s', s)
        record = self.db.fetch_one()
        return record

    def fetch_level_id(self, s):
        self.db.select_one('SELECT id FROM Level WHERE level = %s', s)
        record = self.db.fetch_one()
        return record

    def fetch_department_id(self, s):
        self.db.select_one('SELECT id FROM Department WHERE department = %s', s)
        record = self.db.fetch_one()
        return record

    def fetch_user_name(self, s):
        self.db.select_one('SELECT user_name FROM User WHERE  email= %s', s)
        record = self.db.fetch_one()
        return record

    def fetch_password(self,s):
        self.db.select_one('SELECT password FROM User WHERE email = %s', s)
        record = self.db.fetch_one()
        return record
