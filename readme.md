This is the INSTUCOM API
To setup:
1) Run the requirement.txt file
2) Set the environment variables for :
    a) mysql_host
    b) mysql_password
    c) mysql_user
    d) db_name - (Database name)
    f) jwt_secret_key


It can do fo three major things: 
1) Register a new user
2) get the details of a registered user
3) Loging in


REGISTER A NEW USER
To register a new user, you use the route '/users/register':
The  general user data that are required include:
(a) user_name 
(b) surname 
(c) first_name 
(d) email 
(e) password 
(f) user_type (This must be filled with either 'Student', 'Lecturer' or 'Mentor')

In addition, there are user type specific inputs.
If it's a student, add the following to the data:
(g) program_id
(h) matric_no
(i) program_id


if it's a lecturer, add the following:
(g) department_id
(h) title     (This must be filled with either 'mr', 'mrs', 'miss', 'dr', 'prof')
(i) Position  (This must be filled with either 'juniorlecturer', 'lecturerI', 'lecturerII','seniorlecturer', 'associateprof', 'prof'))

if it's a mentor, add the following:
(g) profession
(h) company
(i) title

Sample registration for a student
user_name   : Popo1
surname     : Oyedeji
first_name  : Emmanuel
email       : emmanueloyedeji20@yahoo.com
password    : Popo1234
user_type   : Student
program_id  : 1
matric_no   : 1233456
program_id  : 3

If input is successful, it returns :                                         {'success': 'succesfully updated in the database'}
If email has been used to register before, it returns:                       {'Error': 'This email has already been used to register'}
If any of the input does not conform to the expected datatype, it returns:   {'Error': 'Unable to retrieve student details. Ensure the inputs are  valid'}  







LOGIN AS A USER
To login, you just need to supply two information in a GET request. The path is '/token/auth':
(a) email
(b) password

Sample 
http://localhost/token/auth
email: emmanueloyedeji20@yahoo.com
password: Popo1234

If login detaials are valid, it returns: "refresh": true,
                                        "user name": "popo1"
            
If either the email or password is wrong, it returns:  "login": false







RETRIEVE A USER DETAIL
NB: To retreive a user detail, you first have to be logged in. 
The routh is '/users/<id>', where 'id' is the id of the user. 
Upon, executing this GET request, it will retrieve all the details associated with this user_id.

Sample
http://localhost/users/5
If user with id 5 exists, it returns:
 "company": "Hollywood",
  "email": "tomcruise@gmail.com",
  "first_name": "Cruise",
  "id": 5,
  "profession": "Actor",
  "surname": "Tom",
  "title": "Mr",
  "user_name": "Tommy",
  "user_type": "Mentor"

if user with id 5 does not exist, it returns: 
  "Error": "User not found"