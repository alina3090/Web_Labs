from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean

from datetime import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base


# Create a DeclarativeMeta instance
Base = declarative_base()


class GUEST(Base):
    __tablename__ = "guest"
    guest_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True
    )
    first_name = Column(String(10))
    last_name = Column(String(20))
    phone = Column(String(20))


class ROOM(Base):
    __tablename__ = "room"
    room_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True
    )
    room_type = Column(String(50))
    price = Integer
    availability = Boolean


class RESERVATION(Base):
    __tablename__ = "reservation"
    reservation_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True
    )
    guest_id = Column(ForeignKey(GUEST.guest_id))
    room_id = Column(ForeignKey(ROOM.room_id))
    check_in_date = Column(DateTime, default=datetime.now())
    check_out_date = Column(DateTime, default=datetime.now())


class SERVICE(Base):
    __tablename__ = "service"
    service_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True
    )
    service_name = Column(String(60))
    price = Column(Integer)


class EMPLOYEE(Base):
    __tablename__ = "employee"
    employee_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True
    )
    first_name = Column(String(10))
    last_name = Column(String(20))
    position = Column(String(20))
