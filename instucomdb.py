import sqlite3

conn = sqlite3.connect('instucomdb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Type')
cur.execute('DROP TABLE IF EXISTS User')
cur.execute('DROP TABLE IF EXISTS Faculty')
cur.execute('DROP TABLE IF EXISTS Department')
cur.execute('DROP TABLE IF EXISTS Program')
cur.execute('DROP TABLE IF EXISTS Level')
cur.execute('DROP TABLE IF EXISTS Student')
cur.execute('DROP TABLE IF EXISTS Lec_Title')
cur.execute('DROP TABLE IF EXISTS Lec_Position')
cur.execute('DROP TABLE IF EXISTS Lecturer')
cur.execute('DROP TABLE IF EXISTS Mentor')



cur.execute('''CREATE TABLE Type (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   type VARCHAR(50) UNIQUE
                                   )''')

cur.execute('''CREATE TABLE User (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   user_name VARCHAR(50),
                                   surname VARCHAR(50),
                                   first_name VARCHAR(50),
                                   email VARCHAR(50) UNIQUE,
                                   password VARCHAR(50),
                                   type_id VARCHAR(50),
                                   FOREIGN KEY (type_id) REFERENCES Type(id)
                                   )''')


cur.execute('''CREATE TABLE School (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   school_name VARCHAR(100) UNIQUE
                                   )''')


cur.execute('''CREATE TABLE Faculty (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   faculty VARCHAR(50) UNIQUE,
                                   school_id INTEGER,
                                   FOREIGN KEY (school_id) REFERENCES School(id)
                                   )''')


cur.execute('''CREATE TABLE Department (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   department VARCHAR(50) UNIQUE,
                                   faculty_id INTEGER,
                                   FOREIGN KEY (faculty_id) REFERENCES Faculty(id)
                                   )''')


cur.execute('''CREATE TABLE Program (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   program VARCHAR(50) UNIQUE,
                                   department_id INTEGER,
                                   FOREIGN KEY (department_id) REFERENCES Department(id)
                                   )''')


cur.execute('''CREATE TABLE Level (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   level INTEGER UNIQUE
                                   )''')

cur.execute('''CREATE TABLE Student (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   user_id INTEGER UNIQUE,
                                   program_id INTEGER
                                   matric_no INTEGER UNIQUE,
                                   level_id INTEGER,
                                   FOREIGN KEY (user_id) REFERENCES User(id),
                                   FOREIGN KEY (program_id) REFERENCES Program(id),
                                   FOREIGN KEY (level_id) REFERENCES Level(id)
                                   )''')

cur.execute('''CREATE TABLE Lec_Title (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   title VARCHAR(50) UNIQUE
                                   )''')

cur.execute('''CREATE TABLE Lec_Position (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   position VARCHAR(50) UNIQUE
                                   )''')

cur.execute('''CREATE TABLE Lecturer (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   user_id INTEGER UNIQUE,
                                   department_id INTEGER,
                                   title_id INTEGER,
                                   position_id INTEGER,
                                   FOREIGN KEY (user_id) REFERENCES User(id),
                                   FOREIGN KEY (department_id) REFERENCES Department(id),
                                   FOREIGN KEY (title_id) REFERENCES Lec_Title(id),
                                   FOREIGN KEY (position_id) REFERENCES Lec_Position(id)
                                   )''')


cur.execute('''CREATE TABLE Mentor (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   user_id INTEGER UNIQUE,
                                   profession VARCHAR(50),
                                   company   VARCHAR(50),
                                   title VARCHAR(50),
                                   FOREIGN KEY (user_id) REFERENCES User(id)
                                   )''')


conn.commit()
conn.close()
