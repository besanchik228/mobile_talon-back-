from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from models import *
from routers.auth_router import router as auth_router
from routers.teacher_router import router as teacher_router
from routers.canteen_router import router as canteen_router
from routers.profile_router import router as profile_router

# Создаём экземпляр приложения FastAPI
app = FastAPI(title="Mobile Talon API")

# Разрешённые источники (CORS)
# Это нужно, чтобы фронтенд мог обращаться к API
origins = [
    None
]

# Подключаем middleware для обработки CORS-запросов
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Разрешённые источники
    allow_credentials=True,       # Разрешаем передачу cookies/авторизационных заголовков
    allow_methods=["*"],          # Разрешаем все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],          # Разрешаем все заголовки
)

# Создание таблиц в базе данных (если их ещё нет)
# Base.metadata содержит все модели, унаследованные от declarative_base()
Base.metadata.create_all(bind=engine)

# Подключаем роутеры (разделяем API по функциональности)
app.include_router(auth_router)      # Авторизация и регистрация
app.include_router(profile_router)   # Работа с профилем пользователя
app.include_router(teacher_router)   # Эндпоинты для учителей
app.include_router(canteen_router)   # Эндпоинты для столовых
