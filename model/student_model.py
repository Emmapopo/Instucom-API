from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .user_model import User


class Student(User, Base, SerializerMixin):
    __tablename__ = 'student'
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    program_id = Column('program_id', Integer, nullable=True)
    matric_no = Column('matric_no', String(50), nullable=True)
    level_id = Column('level_id', Integer, nullable=True)

    serialize_only = ('id', 'user_name', 'surname', 'first_name',
                      'email', 'user_type', 'program_id', 'matric_no', 'level_id')

    __mapper_args__ = {
        'polymorphic_identity': 'Student'
    }

    def __init__(self, user_name=None, surname=None, first_name=None, email=None, password=None, user_type=None, program_id=None, matric_no=None, level_id=None):
        super(Student, self).__init__(user_name, surname,
                                      first_name, email, password, user_type)

        self.program_id = program_id
        self.matric_no = matric_no
        self.level_id = level_id
