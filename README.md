# 📱 Mobile Talon API

FastAPI‑приложение для управления школьными талонами на питание.  
Система поддерживает роли **учитель** и **столовая**, регистрацию, авторизацию, подачу талонов и агрегированные отчёты.

---

## 🚀 Возможности

- 🔑 **Аутентификация и авторизация** (JWT, роли `teacher` и `canteen`)
- 🏫 **Регистрация** столовых и учителей
- 👤 **Профиль пользователя** (просмотр и обновление)
- 🎟 **Талоны**:
  - Учитель подаёт талоны (платные и льготные)
  - Просмотр истории за неделю
- 📊 **Отчёты для столовой**:
  - Сводка за день (по классам)
  - Сводка за неделю (по дням)

---

## 🛠 Технологии

- [FastAPI](https://fastapi.tiangolo.com/) — веб‑фреймворк
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- [Pydantic v2](https://docs.pydantic.dev/) — валидация данных
- [Passlib](https://passlib.readthedocs.io/) — хэширование паролей
- [python-jose](https://python-jose.readthedocs.io/) — JWT
- SQLite (по умолчанию, можно заменить)

---

## 📂 Структура проекта

```
.
├── main.py              # Точка входа в приложение
├── database.py          # Подключение к БД и сессии
├── models.py            # ORM-модели (User, Ticket)
├── schemas.py           # Pydantic-схемы (запросы/ответы)
├── routers/             # Маршруты API
│   ├── auth_router.py
│   ├── profile_router.py
│   ├── teacher_router.py
│   ├── canteen_router.py
│   └── login_router.py
├── environ_init.py      # Конфигурация (SECRET_KEY, DB URL и т.д.)
├── database.db          # SQLite база (локально)
└── .env                 # Переменные окружения
```

---

## ⚙️ Установка и запуск

1. **Клонируем репозиторий:**
   ```bash
   git clone https://github.com/yourname/mobile-talon-api.git
   cd mobile-talon-api
   ```

2. **Создаём виртуальное окружение и активируем его:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   ```

3. **Устанавливаем зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настраиваем .env**

5. **Запускаем сервер:**
   ```bash
   uvicorn main:app --reload
   ```

---

## 📖 Документация API

После запуска доступна по адресу:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔐 Примеры запросов

### 1. Авторизация

```http
POST /auth/login
Content-Type: application/json

{
  "login": "teacher1",
  "password": "1234"
}
```

**Ответ:**

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "role": "teacher"
}
```

### 2. Подача талона (учитель)

```http
POST /talon/submit
Authorization: Bearer <token>
Content-Type: application/json

{
  "date": "2025-09-25",
  "paid_count": 20,
  "free_count": 5
}

```

### И так далее(в папке examples_req)

```