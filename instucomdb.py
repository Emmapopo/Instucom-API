import mysql.connector

mydb = None

try:
    mydb = mysql.connector.connect(
      host= os.environ.get('MYSQL_HOST'),
      user= os.environ.get('MYSQL_USER'),
      passwd= os.environ.get('MYSQL_PASSWORD'),
      database= os.environ.get('MYSQL_DB')
      )
except Exception as e:
    print(e)
    raise e


cur = mydb.cursor()


cur.execute('DROP TABLE IF EXISTS Student')
cur.execute('DROP TABLE IF EXISTS Lecturer')
cur.execute('DROP TABLE IF EXISTS Mentor')
cur.execute('DROP TABLE IF EXISTS Program')
cur.execute('DROP TABLE IF EXISTS Department')
cur.execute('DROP TABLE IF EXISTS Faculty')
cur.execute('DROP TABLE IF EXISTS School')
cur.execute('DROP TABLE IF EXISTS User')
cur.execute('DROP TABLE IF EXISTS Level')
cur.execute('DROP TABLE IF EXISTS Lec_Title')
cur.execute('DROP TABLE IF EXISTS Lec_Position')
cur.execute('DROP TABLE IF EXISTS Lecturer')
cur.execute('DROP TABLE IF EXISTS Mentor')


cur.execute('''CREATE TABLE User (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                   user_name VARCHAR(50),
                                   surname VARCHAR(50),
                                   first_name VARCHAR(50),
                                   email VARCHAR(50) UNIQUE,
                                   password VARCHAR(50),
                                   user_type ENUM('Student', 'Lecturer', 'Mentor')
                                   )''')


cur.execute('''CREATE TABLE School (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                   school_name VARCHAR(100) UNIQUE
                                   )''')


cur.execute('''CREATE TABLE Faculty (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                   faculty VARCHAR(50) UNIQUE,
                                   school_id INTEGER,
                                   FOREIGN KEY (school_id) REFERENCES School(id)
                                   )''')


cur.execute('''CREATE TABLE Department (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                   department VARCHAR(50) UNIQUE,
                                   faculty_id INTEGER,
                                   FOREIGN KEY (faculty_id) REFERENCES Faculty(id)
                                   )''')


cur.execute('''CREATE TABLE Program (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                   program VARCHAR(50) UNIQUE,
                                   department_id INTEGER,
                                   FOREIGN KEY (department_id) REFERENCES Department(id)
                                   )''')


cur.execute('''CREATE TABLE Level (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                   level VARCHAR(50)
                                   )''')

cur.execute('''CREATE TABLE Student (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                   user_id INTEGER UNIQUE,
                                   program_id INTEGER,
                                   matric_no VARCHAR(50) UNIQUE,
                                   level_id INTEGER,
                                   FOREIGN KEY (user_id) REFERENCES User(id),
                                   FOREIGN KEY (program_id) REFERENCES Program(id),
                                   FOREIGN KEY (level_id) REFERENCES Level(id)
                                   )''')


cur.execute('''CREATE TABLE Lecturer (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                   user_id INTEGER UNIQUE,
                                   department_id INTEGER,
                                   title ENUM('Mr', 'Mrs', 'Miss', 'Dr', 'Prof'),
                                   position ENUM ('Junior Lecturer', 'Leturer I', 'Lecturer II', 'Senoir Lecturer', 'Associate Prof', 'Prof'),
                                   FOREIGN KEY (user_id) REFERENCES User(id),
                                   FOREIGN KEY (department_id) REFERENCES Department(id)
                                   )''')


cur.execute('''CREATE TABLE Mentor (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                   user_id INTEGER UNIQUE,
                                   profession VARCHAR(50),
                                   company   VARCHAR(50),
                                   title VARCHAR(50),
                                   FOREIGN KEY (user_id) REFERENCES User(id)
                                   )''')


cur.close()
