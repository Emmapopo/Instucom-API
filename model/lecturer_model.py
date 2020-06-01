
from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .user_model import User


class Lecturer(User, Base, SerializerMixin):
    __tablename__ = 'lecturer'
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    department_id = Column('department_id', Integer, nullable=True)
    title = Column('title', String(50), nullable=True)
    position = Column('position', String(50), nullable=True)

    # User.id, User.user_name, User.surname, User.first_name, User.email, User.password, User.user_type

    serialize_only = ('id', 'user_name', 'surname', 'first_name', 'email', 'user_type', 'department_id', 'title', 'position')

    __mapper_args__ = {
        'polymorphic_identity': 'Lecturer'
    }

    def __init__(self, user_name=None, surname=None, first_name=None, email=None, password=None, user_type=None, department_id=None, title=None, position=None):
        
        super(Lecturer,self).__init__(user_name, surname, first_name, email, password, user_type)

        self.department_id = department_id
        self.title = title
        self.position = position
