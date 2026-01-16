# Pomodoro API Backend

Backend API untuk aplikasi Pomodoro Timer menggunakan FastAPI dengan arsitektur clean code.

## 🚀 Features

- **Authentication**: Register, Login, Refresh Token
- **User Profile**: Get & Update Profile
- **JWT Authentication**: Secure token-based authentication
- **PostgreSQL Database**: Scalable relational database
- **Clean Architecture**: Separation of concerns (Repository, Service, Controller)

## 📁 Project Structure

```
pomodoro-backend/
├── app/
│   ├── api/                 # API Routes (Controllers)
│   │   ├── __init__.py
│   │   └── auth.py          # Auth endpoints
│   ├── core/                # Core configurations
│   │   ├── __init__.py
│   │   ├── config.py        # App settings
│   │   ├── database.py      # Database connection
│   │   ├── dependencies.py  # FastAPI dependencies
│   │   └── security.py      # JWT & Password utils
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   └── user.py          # User model
│   ├── repositories/        # Data access layer
│   │   ├── __init__.py
│   │   └── user_repository.py
│   ├── schemas/             # Pydantic DTOs
│   │   ├── __init__.py
│   │   └── user.py          # Request/Response schemas
│   ├── services/            # Business logic layer
│   │   ├── __init__.py
│   │   └── user_service.py  # Auth & User services
│   ├── __init__.py
│   └── main.py              # FastAPI application
├── alembic/                 # Database migrations
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── .env.example             # Environment template
├── .gitignore
├── alembic.ini              # Alembic config
├── Makefile                 # Commands
├── README.md
└── requirements.txt         # Dependencies
```

## 🛠️ Requirements

- Python 3.10+
- PostgreSQL 12+

## ⚡ Quick Start

### 1. Clone & Setup Environment

```bash
# Clone repository
git clone <repository-url>
cd pomodoro-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your database credentials
nano .env
```

### 3. Install & Run

```bash
# Install dependencies & run migrations
make setup

# Start development server
make dev
```

Server akan berjalan di `http://localhost:8000`

📖 **API Documentation**: 
Setelah server berjalan, buka `http://localhost:8000/docs` untuk melihat Swagger UI interaktif.

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies |
| `make dev` | Run development server with hot reload |
| `make run` | Run production server |
| `make migrate` | Create new migration |
| `make upgrade` | Apply all migrations |
| `make downgrade` | Rollback last migration |
| `make freeze` | Update requirements.txt |
| `make clean` | Clean cache files |
| `make setup` | Initial setup (install + upgrade) |

## 🔗 API Endpoints

### Health Check
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Detailed health check |

### Authentication
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Register new user | ❌ |
| POST | `/api/v1/auth/login` | Login & get tokens | ❌ |
| POST | `/api/v1/auth/refresh` | Refresh access token | ❌ |
| GET | `/api/v1/auth/me` | Get current user profile | ✅ |
| PUT | `/api/v1/auth/me` | Update current user profile | ✅ |
| GET | `/api/v1/auth/profile/{user_id}` | Get user by ID | ❌ |
| POST | `/api/v1/auth/logout` | Logout (stateless) | ✅ |

### Pomodoro
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/pomodoro/sessions` | Create new session | ✅ |
| GET | `/api/v1/pomodoro/history` | Get session history | ✅ |
| GET | `/api/v1/leaderboard` | Get leaderboard | ❌ |

## 📝 API Examples

### Register
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepass123",
    "full_name": "John Doe"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

### Get Profile (Authenticated)
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer <access_token>"
```

### Update Profile
```bash
curl -X PUT "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Updated",
    "avatar_url": "https://example.com/avatar.jpg"
  }'
```

## 📚 API Documentation

Setelah server berjalan, akses dokumentasi interaktif:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗄️ Database Configuration

Edit file `.env` untuk mengkonfigurasi database PostgreSQL:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/pomodoro_db
```

### Create Database

```sql
CREATE DATABASE pomodoro_db;
```

## 🔐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | - |
| `JWT_SECRET_KEY` | Secret key for JWT | - |
| `JWT_ALGORITHM` | JWT algorithm | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiry | 30 |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiry | 7 |
| `APP_NAME` | Application name | Pomodoro API |
| `APP_VERSION` | Application version | 1.0.0 |
| `DEBUG` | Debug mode | True |

## 🏗️ Architecture

Project ini menggunakan **Clean Architecture** dengan layer:

1. **API Layer (Controllers)**: Handle HTTP requests/responses
2. **Service Layer**: Business logic
3. **Repository Layer**: Data access
4. **Models**: Database entities
5. **Schemas**: DTOs (Data Transfer Objects)

```
Request → Controller → Service → Repository → Database
                ↓
Response ← Controller ← Service ← Repository ← Database
```

## 📄 License

MIT License
