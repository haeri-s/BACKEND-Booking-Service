import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType
from server.database import DBBase, engine

class SubscriptionDB(DBBase):
    __tablename__ = 'Subscription'

    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(EmailType, unique=True)
    name = Column(sqlalchemy.String)
    mobile_country_code = Column(sqlalchemy.String(3), default="82")
    mobile = Column(sqlalchemy.String)
    created_at = Column(sqlalchemy.DateTime(timezone=True), server_default=func.now())
    updated_at = Column(sqlalchemy.DateTime(timezone=True), onupdate=func.now())

SubscriptionDB.metadata.create_all(engine)