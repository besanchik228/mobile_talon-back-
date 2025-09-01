from datetime import date
from pydantic import BaseModel, Field
from schemas import UserRole
from typing import Optional, List

#TokenResponde - просто токен и роль юзера
#LoginRequest - логин и пароль для входа
#RegisterCanteenRequest - логин, пароль и гуо для регистрации столовой
#RegisterTeacherRequest - логин, пароль, гуо, id столовой и название класса для регистрации учителя
#GetUser - модель для получения юзера (хранится в базе данных)
#TalonOut - модель для вывода талонов (хранится в базе данных)
#Talon - модель для создания талона
#Daily - модель для вывода дневных отчетов
#DailySummary - модель для вывода суммарного отчета
#DailyTable - модель для вывода таблицы дневных отчетов
#WeeklyTable - модель для вывода таблицы недельных отчетов

#-------- Auth --------

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: UserRole

class LoginRequest(BaseModel):
    login: str
    password: str

class RegisterCanteenRequest(BaseModel):
    login: str
    password: str
    edu: str

class RegisterTeacherRequest(BaseModel):
    login: str
    password: str
    edu: str
    canteen_id: int
    class_name: str

class GetUser(BaseModel):
    id: int
    login: str
    edu: str
    canteen_id: Optional[int] = None
    class_name: Optional[str] = None

    class Config:
        orm_mode = True

#-------- Talons --------

class Talon(BaseModel):
    date: Optional[date] = None
    paid_count: int = Field(ge=0)
    free_count: int = Field(ge=0)

class TalonOut(BaseModel):
    id: int
    date: date
    class_name: str
    paid_count: int
    free_count: int
    total: int

    class Config:
        orm_mode = True

#-------- Out for canteen --------

class Daily(BaseModel):
    class_name: str
    paid_count: int
    free_count: int
    total: int


class DailySummary(BaseModel):
    total_paid: int
    total_free: int
    total_all: int

class DailyTable(BaseModel):
    date: date
    rows: List[DailyCanteen]
    summary: DailySummary

class WeeklyTable(BaseModel):
    first_date: date
    second_date: date
    days: List[DailyTable]