from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
import enum


# Перечисление ролей пользователей
class UserRole(str, enum.Enum):
    teacher = "teacher"   # Учитель
    canteen = "canteen"   # Столовая


class User(Base):
    __tablename__ = "users"   # Название таблицы в БД

    # Основные поля
    id = Column(Integer, primary_key=True, index=True)              # Уникальный ID пользователя
    login = Column(String, unique=True, index=True, nullable=False) # Логин (уникальный)
    hashed_password = Column(String, nullable=False)                # Хэшированный пароль
    educational_institution = Column(String, nullable=False)        # Учебное заведение
    role = Column(Enum(UserRole), nullable=False)                   # Роль (teacher / canteen)

    # Дополнительные поля (актуальны только для учителей)
    class_name = Column(String, nullable=True)                      # Название класса (например "7'В'")
    canteen_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # Ссылка на столовую (User с ролью canteen)

    # Связи
    canteen = relationship("User", remote_side=[id], uselist=False) # Связь "учитель -> столовая"
    tickets = relationship("Ticket", back_populates="teacher")      # Связь "учитель -> талоны"


class Ticket(Base):
    __tablename__ = "tickets"   # Таблица для хранения талонов

    # Основные поля
    id = Column(Integer, primary_key=True, index=True)   # Уникальный ID талона
    date = Column(Date, index=True, nullable=False)      # Дата талона

    paid_count = Column(Integer, nullable=False)         # Количество платных талонов
    free_count = Column(Integer, nullable=False)         # Количество бесплатных (льготных) талонов

    class_name = Column(String, nullable=False)          # Класс, для которого подан талон

    # Связь с учителем
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    teacher = relationship("User", back_populates="tickets")

    # Ограничение: один учитель может подать только один талон на конкретную дату
    __table_args__ = (
        UniqueConstraint("teacher_id", "date", name="uq_ticket_teacher_date"),
    )
