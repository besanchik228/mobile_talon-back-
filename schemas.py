from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field
from models import UserRole


# --------- Auth & Users ---------
class TokenResponse(BaseModel):
    """
    Ответ при успешной авторизации.
    - access_token: сам JWT-токен
    - token_type: тип токена (обычно "bearer")
    - role: роль пользователя (teacher / canteen)
    """
    access_token: str
    token_type: str = "bearer"
    role: UserRole


class LoginRequest(BaseModel):
    """
    Запрос на вход в систему.
    """
    login: str
    password: str


class RegisterCanteenRequest(BaseModel):
    """
    Запрос на регистрацию столовой.
    """
    login: str
    password: str
    educational_institution: str


class RegisterTeacherRequest(BaseModel):
    """
    Запрос на регистрацию учителя.
    """
    login: str
    password: str
    educational_institution: str
    canteen_id: int   # ID столовой, к которой привязан учитель
    class_name: str   # Название класса (например "7А")


class UserPublic(BaseModel):
    """
    Публичное представление пользователя (возвращается в ответах).
    """
    id: int
    login: str
    role: UserRole
    educational_institution: str
    class_name: Optional[str] = None
    canteen_id: Optional[int] = None

    class Config:
        from_attributes = True  # Позволяет создавать схему напрямую из ORM-модели


class ProfileUpdate(BaseModel):
    """
    Запрос на обновление профиля.
    - educational_institution: новое учебное заведение
    - password: новый пароль (минимум 4 символа)
    - class_name, canteen_id: доступны только для учителей
    """
    educational_institution: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=4)
    class_name: Optional[str] = None
    canteen_id: Optional[int] = None


# --------- Tickets ---------
class TicketCreate(BaseModel):
    """
    Запрос на создание талона.
    - date: дата (по умолчанию сегодня)
    - paid_count: количество платных талонов
    - free_count: количество бесплатных (льготных) талонов
    """
    date: Optional[date] = None
    paid_count: int = Field(ge=0)   # ge=0 — не может быть отрицательным
    free_count: int = Field(ge=0)


class TicketOut(BaseModel):
    """
    Ответ с информацией о талоне.
    """
    id: int
    date: date
    class_name: str
    paid_count: int
    free_count: int
    total: int   # общее количество (paid + free)

    class Config:
        from_attributes = True


# --------- Aggregations (агрегации для столовой) ---------
class CanteenDayRow(BaseModel):
    """
    Строка отчёта по одному классу за день.
    """
    class_name: str
    paid_count: int
    free_count: int
    total: int


class CanteenDaySummary(BaseModel):
    """
    Итоговая сводка за день по всем классам.
    """
    total_paid: int
    total_free: int
    total_all: int


class CanteenDayResponse(BaseModel):
    """
    Ответ для отчёта за день.
    - date: дата отчёта
    - rows: список классов с их талонами
    - summary: общая сводка
    """
    date: date
    rows: List[CanteenDayRow]
    summary: CanteenDaySummary


class CanteenWeekDay(BaseModel):
    """
    Данные по одному дню недели.
    """
    date: date
    total_paid: int
    total_free: int
    total_all: int


class CanteenWeekResponse(BaseModel):
    """
    Ответ для недельного отчёта.
    - start_date, end_date: диапазон дат
    - days: список дней с данными
    - grand_total_*: общие суммы за неделю
    """
    start_date: date
    end_date: date
    days: List[CanteenWeekDay]
    grand_total_paid: int
    grand_total_free: int
    grand_total_all: int
