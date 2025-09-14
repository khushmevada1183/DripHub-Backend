# 🔥 DripHub - Modern E-commerce Backend

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

*A blazingly fast, production-ready e-commerce backend built with modern Python stack*

[🚀 Quick Start](#-quick-start) • [📚 API Docs](#-api-documentation) • [🛠️ Development](#-development) • [🐳 Docker](#-docker) • [🔧 Configuration](#-configuration)

</div>

---

## ✨ Features

### 🔐 **Authentication & Security**
- **JWT Token Authentication** - Secure stateless authentication
- **Supabase Integration** - Modern auth provider support
- **Password Hashing** - bcrypt encryption for user passwords
- **CORS Enabled** - Cross-origin resource sharing configured

### 🛒 **E-commerce Core**
- **User Management** - Registration, profiles, and user data
- **Product Catalog** - Complete product management system
- **Order Processing** - Full order lifecycle management
- **RESTful API** - Clean, intuitive API design

### 🏗️ **Architecture**
- **Clean Architecture** - Separation of concerns with CRUD, schemas, and models
- **Database Agnostic** - SQLAlchemy ORM with support for multiple databases
- **Error Handling** - Consistent error responses with proper HTTP status codes
- **Validation** - Pydantic models for request/response validation
- **Type Safety** - Full Python type hints throughout

### 🚀 **Performance & Scalability**
- **Async Support** - Built on FastAPI's async foundation
- **Auto-Generated Docs** - Interactive OpenAPI/Swagger documentation
- **Hot Reload** - Development server with automatic reloading
- **Docker Ready** - Containerized for easy deployment

---

## 📋 Prerequisites

- **Python 3.8+** (3.13 recommended)
- **Git** for version control
- **Docker** (optional, for containerized deployment)

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/khushmevada1183/ecommerce_driphub.git
cd ecommerce_driphub
```

### 2️⃣ Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (Command Prompt)
.venv\Scripts\activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (Git Bash)
source .venv/Scripts/activate
# macOS/Linux
source .venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
```

### 5️⃣ Launch the Server
```bash
# Development server with hot reload
uvicorn app.main:app --app-dir src --reload --port 8000

# Production server
uvicorn app.main:app --app-dir src --host 0.0.0.0 --port 8000
```

🎉 **Your API is now running at** → http://localhost:8000

---

## 📚 API Documentation

### 🔍 Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### 🔗 Core Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/` | Health check | ❌ |
| `POST` | `/api/auth/register` | User registration | ❌ |
| `POST` | `/api/auth/login` | User login | ❌ |
| `GET` | `/api/users/me` | Get current user | ✅ |
| `GET` | `/api/products/` | List products | ✅ |
| `POST` | `/api/products/` | Create product | ✅ |
| `POST` | `/api/orders/` | Create order | ✅ |
| `GET` | `/api/orders/{id}` | Get order details | ✅ |

### 📝 Request/Response Examples

<details>
<summary><strong>🔐 User Registration</strong></summary>

**Request:**
```json
POST /api/auth/register
{
  "email": "user@driphub.com",
  "password": "secure_password_123"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@driphub.com",
  "is_active": true,
  "is_superuser": false
}
```
</details>

<details>
<summary><strong>🔑 User Login</strong></summary>

**Request:**
```json
POST /api/auth/login
{
  "username": "user@driphub.com",
  "password": "secure_password_123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```
</details>

<details>
<summary><strong>🛒 Create Order</strong></summary>

**Request:**
```json
POST /api/orders/
Authorization: Bearer {your_token}
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "total": 29.99,
  "status": "pending",
  "created_at": "2025-08-30T12:00:00Z"
}
```
</details>

---

## 🛠️ Development

### 📁 Project Structure
```
📦 DripHub Backend
├── 📁 app/
│   ├── 📁 api/
│   │   └── 📁 api_v1/
│   │       ├── 📁 routers/
│   │       │   ├── auth.py      # Authentication endpoints
│   │       │   ├── users.py     # User management
│   │       │   ├── products.py  # Product catalog
│   │       │   └── orders.py    # Order processing
│   │       └── api.py           # API router aggregation
│   ├── 📁 core/
│   │   ├── config.py            # Application configuration
│   │   ├── security.py          # JWT and password handling
│   │   ├── exceptions.py        # Custom exception classes
│   │   └── supabase_auth.py     # Supabase integration
│   ├── 📁 crud/
│   │   ├── crud_user.py         # User database operations
│   │   ├── crud_product.py      # Product database operations
│   │   └── crud_order.py        # Order database operations
│   ├── 📁 db/
│   │   ├── base.py              # Database models registry
│   │   └── session.py           # Database session management
│   ├── 📁 models/
│   │   ├── user.py              # User database model
│   │   ├── product.py           # Product database model
│   │   └── order.py             # Order database model
│   ├── 📁 schemas/
│   │   ├── user.py              # User Pydantic schemas
│   │   ├── product.py           # Product Pydantic schemas
│   │   └── order.py             # Order Pydantic schemas
│   └── main.py                  # FastAPI application entry point
├── 📁 tests/
│   └── test_basic.py            # Basic API tests
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container configuration
├── Makefile                     # Development commands
└── README.md                    # This file
```

### 🧪 Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_basic.py -v
```

### 🔍 Code Quality
```bash
# Format code with black
black app/

# Lint with flake8
flake8 app/

# Type checking with mypy
mypy app/
```

---

## 🔧 Configuration

### 📄 Environment Variables

Create a `.env` file in the project root:

```bash
# Application
PROJECT_NAME="DripHub Backend"
API_V1_STR="/api"
SECRET_KEY="your-super-secret-jwt-key-here"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL="sqlite:///./app.db"

# Supabase (Optional)
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_ANON_KEY="your-anon-key"
SUPABASE_SERVICE_ROLE_KEY="your-service-role-key"
```

### ⚙️ Configuration Options

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PROJECT_NAME` | Application name | "DripHub Backend" | ❌ |
| `SECRET_KEY` | JWT signing key | "change-this-secret" | ✅ |
| `DATABASE_URL` | Database connection string | `None` | ✅ |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiration time | 30 | ❌ |
| `SUPABASE_URL` | Supabase project URL | `""` | ❌ |

---

## 🐳 Docker

### 🚀 Quick Docker Setup
```bash
# Build the image
docker build -t driphub-backend .

# Run the container
docker run -p 8000:8000 --env-file .env driphub-backend
```

### 🐙 Docker Compose (Recommended)
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/driphub
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=driphub
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api
```

---

## 🚀 Deployment

### 🌐 Production Checklist

- [ ] Set strong `SECRET_KEY` in production
- [ ] Use production database (PostgreSQL recommended)
- [ ] Enable HTTPS/TLS encryption
- [ ] Configure proper CORS origins
- [ ] Set up monitoring and logging
- [ ] Implement rate limiting
- [ ] Use environment variables for secrets
- [ ] Enable database connection pooling

### ☁️ Platform Deployments

<details>
<summary><strong>🔷 Railway</strong></summary>

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```
</details>

---

## 🧭 Run & DB troubleshooting

If your deployed web service starts but registration or other DB-backed endpoints return errors, use the following checks and recommendations.

1. Quick health endpoints

- Lightweight process health (no DB access):

  GET /health

  - Returns 200 {"status":"ok"} when the process is running. This intentionally avoids touching the DB so the process can be considered alive even if the database is unreachable.

- Database connectivity check (minimal):

  GET /health/db

  - Returns 200 {"status":"ok","db":"reachable"} when a simple SQL `SELECT 1` succeeds.
  - Returns 503 {"status":"unavailable","db":"unreachable"} when the DB is not reachable.

2. Typical failure and quick interpretation

- If `/health` is 200 but `/health/db` is 503 and DB-backed endpoints (e.g. `/api/auth/register`) return 503 or 500, the web service cannot open a TCP connection to your database. The error in logs usually looks like `psycopg2.OperationalError: ... Network is unreachable`.

- Possible causes:
  - Wrong `DATABASE_URL` or credentials.
  - Network ACLs / firewall / VPC rules that prevent the Render instance from reaching the DB host.
  - The DB service is down or not accepting connections on the configured host/port.

3. How to debug from Render (recommended)

- Use a one-off shell on Render (or a Render Job) in the same region/network as your web service and try a minimal connect from there. For example, run a short Python snippet or `psql` to validate connectivity.

- If your DB is hosted on Supabase and you see `Network is unreachable`, check whether Supabase requires allowlisting or private networking and whether Render's outbound IP ranges are allowed.

4. Migrations: where to run them

- Prefer running migrations separately from the web workers. Options:
  - Render Job / one-off: create a Render Job (or a one-off shell) that runs `alembic upgrade head` in the same network as the DB. This is reliable when the Render environment can access the database.
  - Self-hosted CI runner: run migrations from a self-hosted runner (GitHub Actions self-hosted) that has network access to your DB.
  - Manual: run migrations locally from a machine that can reach the DB (less automated but simple).

- Don't run `Base.metadata.create_all()` on web startup in production; use migrations instead. This project already supports skipping DB init at startup via the `SKIP_DB_INIT` env var.

5. Quick commands

Run the DB health check (from anywhere):

```bash
# Lightweight health (process):
curl -i https://<your-host>/health

# DB reachability check (from the same network as the service):
curl -i https://<your-host>/health/db
```

Run migrations (example; ensure `DATABASE_URL` is set and reachable):

```bash
# from project root
alembic upgrade head
```


<details>
<summary><strong>🟦 Vercel</strong></summary>

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```
</details>

<details>
<summary><strong>🟣 Heroku</strong></summary>

```bash
# Create Heroku app
heroku create driphub-backend

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku main
```
</details>

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### 📝 Development Guidelines
- Follow PEP 8 style guide
- Add type hints to all functions
- Write tests for new features
- Update documentation as needed
- Use meaningful commit messages

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 💬 Support

<div align="center">

**Questions? Issues? Suggestions?**

[![GitHub Issues](https://img.shields.io/github/issues/khushmevada1183/ecommerce_driphub?style=for-the-badge)](https://github.com/khushmevada1183/ecommerce_driphub/issues)
[![GitHub Discussions](https://img.shields.io/github/discussions/khushmevada1183/ecommerce_driphub?style=for-the-badge)](https://github.com/khushmevada1183/ecommerce_driphub/discussions)

*Built with ❤️ by [Khush Mevada](https://github.com/khushmevada1183)*

</div>

---

<div align="center">

**⭐ Star this repo if you find it useful!**

*Made with FastAPI 🚀 | Powered by Python 🐍 | Designed for Scale 📈*

</div>