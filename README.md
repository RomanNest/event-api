# Event API

🚀 Асинхронний REST API сервіс для керування подіями та бронюваннями з авторизацією через JWT.

## ⚙️ Стек технологій

- **Python 3.12**
- **FastAPI**
- **PostgreSQL**
- **Async SQLAlchemy**
- **Alembic**
- **Poetry**
- **JWT (Bearer Token Auth)**

---

## 🏁 Швидкий старт

### 1. Клонування репозиторію
```bash
git clone https://github.com/RomanNest/event-api.git
cd event-api
```

### 2. Створити `.env` файл
```ini
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/event_db
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> 🔐 Не коміть `.env` у репозиторій.

---

### 3. Встановлення залежностей
```bash
poetry install
```

### 4. Активація середовища
```bash
poetry shell
```

---

### 5. Ініціалізація бази даних

#### Створити міграції:
```bash
alembic revision --autogenerate -m "Initial migration"
```

#### Застосувати міграції:
```bash
alembic upgrade head
```

---

### 6. Запуск сервера
```bash
poetry run uvicorn app.main:app --reload
```

> Додай `--host 0.0.0.0 --port 8000`, якщо хочеш запустити з доступом ззовні.

---


## 🔐 Авторизація

- Використовується **JWT Bearer Token**.
- Отримання токена: `POST /auth/login`
- Захищені роутери потребують:  
  ```
  Authorization: Bearer <your_token>
  ```
## 📌 API ендпоінти

| Метод | Шлях               | Опис                              |
|-------|--------------------|-----------------------------------|
| POST  | /auth/register     | Реєстрація користувача            |
| POST  | /auth/login        | Логін, повертає JWT               |
| GET   | /events/           | Список подій                      |
| POST  | /events/           | Створити подію (JWT)              |
| GET   | /events/my         | Мої події (JWT)                   |
| POST  | /events/{id}/book  | Забронювати місце (JWT)           |
| GET   | /bookings/my       | Мої бронювання (JWT)              |

> 🔐 Ендпоінти з позначкою **(JWT)** потребують заголовок:
> ```
> Authorization: Bearer <your_token>
> ```

---

## 🧪 Документація API

Після запуску доступна інтерактивна документація:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---
