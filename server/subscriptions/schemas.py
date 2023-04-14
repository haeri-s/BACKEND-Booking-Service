import sqlalchemy
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship
from server.database import DBBase, engine

class UserDB(DBBase):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(EmailType)
    name = Column(sqlalchemy.String)
    mobile_country_code = Column(sqlalchemy.String(3), default="82")
    mobile = Column(sqlalchemy.String, unique=True)
    created_at = Column(sqlalchemy.DateTime(timezone=True), server_default=func.now())
    updated_at = Column(sqlalchemy.DateTime(timezone=True), onupdate=func.now())

    subscribes = relationship('UserSubscribeDB', back_populates="user")

class UserSubscribeDB(DBBase):
    __tablename__ = 'user_subscribe'

    id = Column(sqlalchemy.Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    created_at = Column(sqlalchemy.DateTime(timezone=True), server_default=func.now())
    updated_at = Column(sqlalchemy.DateTime(timezone=True), onupdate=func.now())

    user = relationship('UserDB', back_populates="subscribes")

UserDB.metadata.create_all(engine)
UserSubscribeDB.metadata.create_all(engine)