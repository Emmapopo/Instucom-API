
class UserModel():
    def __init__(self, id = None, user_name = None, surname = None, first_name = None, email = None, password = None, user_type = None, user_id = None):
        self.id = id
        self.user_name = user_name
        self.surname = surname
        self.first_name = first_name
        self.email = email
        self.password = password
        self.user_type = user_type
        self.user_id = user_id

    def set_user_name(self, u_n):
        self.user_name = u_n

    def get_user_name(self):
        return self.user_name

    def set_surname(self, sn):
        self.surname = sn

    def get_surname(self):
        return self.surname

    def set_first_name(self, f_n):
        self.first_name = f_n

    def get_first_name(self):
        return self.first_name

    def set_email(self, e):
        self.email = e

    def get_email(self):
        return self.email

    def set_password(self, p):
        self.password = p

    def get_password(self):
        return self.password

    def set_user_type(self, u_t):
        self.user_type = u_t

    def get_user_type(self):
        return self.user_type

    def set_user_id(self, u_id):
        self.user_id = u_id

    def get_user_id(self):
        return self.user_id


class StudentModel(UserModel):
    def __init__(self, program_id = None, department_id = None, faculty_id = None, school_id = None, matric_no = None, level_id = None):
        super().__init__()
        self.program_id = program_id
        self.department_id = department_id
        self.faculty_id = faculty_id
        self.school_id = school_id
        self.matric_no = matric_no
        self.level_id = level_id

    def set_program_id(self, p_id):
        self.program_id = p_id

    def get_program_id(self):
        return self.program_id

    def set_matric_no(self, m_no):
        self.matric_no = m_no

    def get_matric_no(self):
        return self.matric_no

    def set_level_id(self, l_id):
        self.level_id = l_id

    def get_level_id(self):
        return self.level_id


class LecturerModel(UserModel):
    def __init__(self, department_id = None, faculty_id = None, school_id = None, title = None, position = None):
        super().__init__()
        self.department_id = department_id
        self.faculty_id = faculty_id
        self.school_id = school_id
        self.title = title
        self.position = position

    def set_department_id(self, d_id):
        self.department_id = d_id

    def get_department_id(self):
        return self.department_id

    def set_title(self, t):
        self.title = t

    def get_title(self):
        return self.title
    
    def set_position(self, p):
        self.position = p

    def get_position(self):
        return self.position



class MentorModel(UserModel):
    def __init__(self, profession = None, company = None, title = None):
        super().__init__()
        self.profession = profession
        self.company = company
        self.title = title

    def set_profession(self, p):
        self.profession = p

    def get_profession(self):
        return self.profession

    def set_company(self, c):
        self.company = c

    def get_company(self):
        return self.company

    def set_title(self, t):
        self.title = t

    def get_title(self):
        return self.title

    

        
    

    