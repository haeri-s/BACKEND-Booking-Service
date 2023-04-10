import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType, PasswordType
from sqlalchemy.orm import relationship
from server.database import DBBase, engine
import enum
from sqlalchemy.dialects.postgresql import ARRAY

class ServiceCategoryEnum(enum.Enum):
    training = 'training'
    fun = 'fun'
    discovery = 'discovery'

class ServiceCategoryDB(DBBase):
    __tablename__ = 'service_category'
    id = Column(sqlalchemy.Integer, primary_key=True, index=True)
    category = Column(sqlalchemy.Enum(ServiceCategoryEnum), nullable=False, comment='서비스 유형')
    name= Column(sqlalchemy.CHAR(100), nullable=False, comment='서비스 유형명')

    services = relationship('ServiceDB', back_populates="category")
    
    
class DurationUitEnum(enum.Enum):
    day = 'day'
    hour = 'hour'

class ServiceDB(DBBase):
    __tablename__ = 'service'

    id = Column(UUID(as_uuid=True), primary_key=True)
    category_id = Column(sqlalchemy.ForeignKey('service_category.id'))
    name = Column(sqlalchemy.CHAR(200), comment='서비스명')
    price = Column(sqlalchemy.Integer, default=0, comment='기본 서비스 비용')
    notes = Column(sqlalchemy.CHAR(100), nullable=True, comment='서비스 유의사항')

    duration = Column(sqlalchemy.Integer, default=0, comment='소요기간')
    duration_unit = Column(sqlalchemy.Enum(DurationUitEnum), default=DurationUitEnum.hour, comment='소요기간 단위(일/시간)')

    can_choice_hour = Column(sqlalchemy.Boolean, default=False, comment='시간 선택가능 여부')
    can_rental = Column(sqlalchemy.Boolean, default=False, comment='장비렌탈 가능 여부')

    is_disabled = Column(sqlalchemy.Boolean, default=False, comment='예약가능여부')
    is_deleted = Column(sqlalchemy.Boolean, default=False, comment='삭제여부')

    created_at = Column(sqlalchemy.DateTime(timezone=True), server_default=func.now())
    updated_at = Column(sqlalchemy.DateTime(timezone=True), onupdate=func.now())

    category = relationship('ServiceCategoryDB', back_populates="services")

class ServiceNonBookingDay(DBBase):
    __tablename__ = 'service_non_booking_day'

    id = Column(sqlalchemy.Integer, primary_key=True, index=True)
    service_id = Column(sqlalchemy.ForeignKey('service.id'))
    date = Column(sqlalchemy.DATE, nullable=False, comment="예약 불가일")

    created_at = Column(sqlalchemy.DateTime(timezone=True), server_default=func.now())
    updated_at = Column(sqlalchemy.DateTime(timezone=True), onupdate=func.now())


class ServiceRental(DBBase):
    __tablename__ = 'service_rental'

    id = Column(sqlalchemy.Integer, primary_key=True, index=True)
    name = Column(sqlalchemy.CHAR(200), comment='렌탈 상품명')
    price = Column(sqlalchemy.Integer, default=0, comment='비용')
    description = Column(sqlalchemy.Text, comment='설명')

    created_at = Column(sqlalchemy.DateTime(timezone=True), server_default=func.now())
    updated_at = Column(sqlalchemy.DateTime(timezone=True), onupdate=func.now())

# class PayMethodEnum(enum.Enum):
#     card = 'card'
#     bank = 'bank'

# class ServiceSecondaryPriceDB(DBBase):
#     __tablename__ = 'service_secondary_price' 
#
#     id = Column(sqlalchemy.Integer, primary_key=True, index=True)
#     service_id = Column(sqlalchemy.ForeignKey('service.id'))
#     description = Column(sqlalchemy.TEXT, commnt="설명")
#     start_expiration_at = Column(sqlalchemy.DATE, nullable=False, comment='적용 시작일')
#     end_expiration_at = Column(sqlalchemy.DATE, nullable=False, comment='적용 종료일')
#     pay_method = Column(ARRAY(PayMethodEnum), default= PayMethodEnum.card, comment="결제수단")

ServiceDB.metadata.create_all(engine)
