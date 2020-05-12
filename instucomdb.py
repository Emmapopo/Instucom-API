import sqlite3

conn = sqlite3.connect('instucomdb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Status')
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



cur.execute('''CREATE TABLE Status (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   status
                                   )''')

cur.execute('''CREATE TABLE User (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   user_name VARCHAR(50),
                                   surname VARCHAR(50),
                                   first_name VARCHAR(50),
                                   email TEXT,
                                   password VARCHAR(50),
                                   status_id,
                                   FOREIGN KEY (status_id) REFERENCES Status(id)
                                   )''')


cur.execute('''CREATE TABLE School (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   school_name
                                   )''')


cur.execute('''CREATE TABLE Faculty (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   faculty,
                                   school_id,
                                   FOREIGN KEY (school_id) REFERENCES School(id)
                                   )''')


cur.execute('''CREATE TABLE Department (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   department,
                                   faculty_id,
                                   FOREIGN KEY (faculty_id) REFERENCES Faculty(id)
                                   )''')


cur.execute('''CREATE TABLE Program (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   program,
                                   department_id,
                                   FOREIGN KEY (department_id) REFERENCES Department(id)
                                   )''')


cur.execute('''CREATE TABLE Level (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   level
                                   )''')

cur.execute('''CREATE TABLE Student (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   user_id,
                                   program_id,
                                   matric_no,
                                   level_id,
                                   FOREIGN KEY (user_id) REFERENCES User(id),
                                   FOREIGN KEY (program_id) REFERENCES Program(id),
                                   FOREIGN KEY (level_id) REFERENCES Level(id)
                                   )''')

cur.execute('''CREATE TABLE Lec_Title (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   title
                                   )''')

cur.execute('''CREATE TABLE Lec_Position (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   position
                                   )''')

cur.execute('''CREATE TABLE Lecturer (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   user_id,
                                   department_id,
                                   title_id,
                                   position_id,
                                   FOREIGN KEY (user_id) REFERENCES User(id),
                                   FOREIGN KEY (department_id) REFERENCES Department(id),
                                   FOREIGN KEY (title_id) REFERENCES Lec_Title(id),
                                   FOREIGN KEY (position_id) REFERENCES Lec_Position(id)
                                   )''')


cur.execute('''CREATE TABLE Mentor (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   user_id,
                                   profession VARCHAR(50),
                                   company   VARCHAR(50),
                                   title TEXT,
                                   FOREIGN KEY (user_id) REFERENCES User(id)
                                   )''')


conn.commit()
conn.close()
