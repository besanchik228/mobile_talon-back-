from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
import enum


class UserRole(str, enum.Enum):
    teacher = "teacher"
    canteen = "canteen"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    educational_institution = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    # Поля актуальны только для учителя
    class_name = Column(String, nullable=True)                     # например "7'В'"
    canteen_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Связи
    canteen = relationship("User", remote_side=[id], uselist=False)
    tickets = relationship("Ticket", back_populates="teacher")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True, nullable=False)

    paid_count = Column(Integer, nullable=False)
    free_count = Column(Integer, nullable=False)

    class_name = Column(String, nullable=False)

    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    teacher = relationship("User", back_populates="tickets")

    __table_args__ = (
        UniqueConstraint("teacher_id", "date", name="uq_ticket_teacher_date"),
    )
