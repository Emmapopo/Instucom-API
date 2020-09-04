from sqlalchemy import *
from model.base import Base
from sqlalchemy.orm import relationship
from model.user_model import User
from .personal_conv_init import PersonalConvInit


class PersonalConvMem(Base):
    __tablename__ = 'personal_conv_mem'
    id = Column('id', Integer, primary_key=True)
    conv_id = Column('conv_id', Integer, ForeignKey('personal_conv_init.conv_id'))
    member_id = Column('member_id', Integer, ForeignKey('user.id'))

    def __init__(self, conv_id = None, member_id = None):
        self.conv_id = conv_id
        self.member_id = member_id
