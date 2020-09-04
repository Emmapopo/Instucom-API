from sqlalchemy import *
from model.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql
import datetime
from model.user_model import User


class PersonalConvInit(Base):
    __tablename__ = 'personal_conv_init'
    conv_id = Column('conv_id', Integer, primary_key=True)
    initiator_id = Column('initiator_id', Integer, ForeignKey('user.id'))
    timestamp = Column(mysql.DATETIME(fsp=6), default=datetime.datetime.utcnow)

    def __init__(self, initiator_id=None, timestamp=None):
        self.timestamp = timestamp
        self.initiator_id = initiator_id
