import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType, PasswordType
from server.database import DBBase, engine

# manager_tb = sqlalchemy.Table(
#     'Manager',
#     metadata,
#     sqlalchemy.Column("id", UUID(as_uuid=True), primary_key=True),
#     sqlalchemy.Column("email", EmailType, unique=True),
#     sqlalchemy.Column("name", sqlalchemy.String),
#     sqlalchemy.Column("password", PasswordType(
#         schemes=["pbkdf2_sha512", "md5_crypt"], 
#         deprecated=["md5_crypt"]
#     )),
#     sqlalchemy.Column("mobile", PhoneNumberType(region='KR')),
#     sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True), server_default=func.now()),
#     sqlalchemy.Column("updated_at", sqlalchemy.DateTime(timezone=True), onupdate=func.now()),
# )

class ManagerDB(DBBase):
    __tablename__ = 'manager'

    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(EmailType, unique=True)
    name = Column(sqlalchemy.String)
    password = Column(PasswordType(
        schemes=["pbkdf2_sha512", "md5_crypt"], 
        deprecated=["md5_crypt"]
    ))
    mobile = Column(sqlalchemy.String)
    created_at = Column(sqlalchemy.DateTime(timezone=True), server_default=func.now())
    updated_at = Column(sqlalchemy.DateTime(timezone=True), onupdate=func.now())

ManagerDB.metadata.create_all(engine)
