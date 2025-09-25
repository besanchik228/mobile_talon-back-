from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field
from models import UserRole


# --------- Auth & Users ---------
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
    educational_institution: str


class RegisterTeacherRequest(BaseModel):
    login: str
    password: str
    educational_institution: str
    canteen_id: int
    class_name: str


class UserPublic(BaseModel):
    id: int
    login: str
    role: UserRole
    educational_institution: str
    class_name: Optional[str] = None
    canteen_id: Optional[int] = None

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    educational_institution: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=4)
    # поля учителя:
    class_name: Optional[str] = None
    canteen_id: Optional[int] = None


# --------- Tickets ---------
class TicketCreate(BaseModel):
    date: Optional[date] = None
    paid_count: int = Field(ge=0)
    free_count: int = Field(ge=0)


class TicketOut(BaseModel):
    id: int
    date: date
    class_name: str
    paid_count: int
    free_count: int
    total: int

    class Config:
        from_attributes = True


    # --------- Aggregations ---------
class CanteenDayRow(BaseModel):
    class_name: str
    paid_count: int
    free_count: int
    total: int


class CanteenDaySummary(BaseModel):
    total_paid: int
    total_free: int
    total_all: int


class CanteenDayResponse(BaseModel):
    date: date
    rows: List[CanteenDayRow]
    summary: CanteenDaySummary


class CanteenWeekDay(BaseModel):
    date: date
    total_paid: int
    total_free: int
    total_all: int


class CanteenWeekResponse(BaseModel):
    start_date: date
    end_date: date
    days: List[CanteenWeekDay]
    grand_total_paid: int
    grand_total_free: int
    grand_total_all: int
