from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin


class User(Base, SerializerMixin):
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key=True)
    user_name = Column('user_name', String(50), nullable=True)
    surname = Column('surname', String(50), nullable=True)
    first_name = Column('first_name', String(50), nullable=True)
    email = Column('email', String(50), nullable=True)
    password = Column('password', String(50), nullable=True)
    user_type = Column('user_type', String(50), nullable=True)

    serialize_rules = ('-lecturers.user', '-students.user', '-mentors.user')
    
    lecturers = relationship("Lecturer", backref='user')
    students = relationship("Student", backref='user')
    mentors = relationship("Mentor", backref='user')
    
    

    __mapper_args__ = {
        'polymorphic_identity' : 'user',
        'polymorphic_on': user_type
    }

    def __init__(self, user_name=None, surname=None, first_name=None, email=None, password=None, user_type=None):
        self.user_name = user_name
        self.surname = surname
        self.first_name = first_name
        self.email = email
        self.password = password
        self.user_type = user_type







