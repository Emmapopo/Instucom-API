from flask import Flask
from flask_mysqldb import MySQL


class Database:
    def __init__(self, db):
        self.db = db
        self.cur = self.db.connection.cursor()

    def select_one(self, command, *s):
        self.cur.execute(command,*s)

    def insert_one(self, command, *s):
        self.cur.execute(command, *s)
        self.db.connection.commit()

    def fetch_one(self):
        rv = self.cur.fetchone()[0]
        return rv


