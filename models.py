from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
import enum

class UserRole(str, enum.Enum):
    teacher = "teacher"
    canteen = "canteen"