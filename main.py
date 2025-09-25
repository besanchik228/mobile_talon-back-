from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from models import *
from routers.auth_router import router as auth_router
from routers.teacher_router import router as teacher_router
from routers.canteen_router import router as canteen_router
from routers.profile_router import router as profile_router

app = FastAPI(title="Mobile Talon API")

origins = [
    "http://localhost:3000",
    "http://192.168.100.106:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Роуты
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(teacher_router)
app.include_router(canteen_router)
