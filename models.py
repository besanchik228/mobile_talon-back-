from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
import enum

#UserRole - роли
#User - Модель пользователя
#Talon - Модель талона

class UserRole(str, enum.Enum):
    teacher = "teacher"
    canteen = "canteen"

class User(Base):
    __tablename__ = "user"
    #id (int) - id пользователя
    #login (str) - логин пользователя
    #hashed_password (str) - хэш пароля пользователя
    #edu (str) - гуо пользователя
    #role (UserRole) - роль пользователя
    #class_name (str) - класс пользователя
    #canteen_id (int) - id cтоловой, к которой относится пользователь


    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    edu = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    class_name = Column(String, nullable=True)
    canteen_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    canteen = relationship("User", remote_side=[id], uselist=False)
    talons = relationship("Talon", back_populates="teacher")

class Talon(Base):
    __tablename__ = "talon"
    #id (int) - id талона
    #date (date) - дата талона
    #paid_count (int) - количество оплаченных уроков
    #free_count (int) - количество бесплатных уроков
    #class_name (str) - класс, к которому относится талон
    #teacher_id (int) - id учителя, которому принадлежит талон

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)

    paid_count = Column(Integer, nullable=False)
    free_count = Column(Integer, nullable=False)

    class_name = Column(String, nullable=False)

    teacher_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    teacher = relationship("User", back_populates="talons")

    __table_args__ = (
        UniqueConstraint('teacher_id', 'date', name='uq_talon_teacher_date'),
    )