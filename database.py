from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from environ_init import DATA_ADDRESS

# Адрес подключения к базе данных
SQLALCHEMY_DATABASE_URL = DATA_ADDRESS

# Создаём движок SQLAlchemy
# connect_args={"check_same_thread": False} — нужно для SQLite,
# чтобы можно было работать с БД из разных потоков (например, в FastAPI).
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Создаём фабрику сессий для работы с БД
# autocommit=False — изменения не сохраняются автоматически, нужно явно вызывать commit()
# autoflush=False — отключает автоматическую синхронизацию сессии с БД при каждом запросе
# bind=engine — связывает сессии с нашим движком
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей SQLAlchemy
# От него будут наследоваться все ORM-модели (User, Ticket и т.д.)
Base = declarative_base()


def get_db():
    """
    Dependency для FastAPI.
    Создаёт новую сессию БД для каждого запроса и закрывает её после завершения.
    Используется через Depends(get_db).
    """
    db = SessionLocal()
    try:
        yield db   # отдаём сессию в эндпоинт
    finally:
        db.close()  # после завершения запроса сессия закрывается
