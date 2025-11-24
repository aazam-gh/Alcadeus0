# Backend Setup Guide

This document provides comprehensive instructions for setting up and running the Field Solutions Management backend service.

## Project Structure

The repository is organized as a mono-repo with a dedicated `/backend` service:

```
project/
├── README.md                 # Original GitHub profile README
├── .env                      # Local environment configuration (git-ignored)
├── .env.example              # Template for environment variables
├── .gitignore                # Git ignore rules
├── Makefile                  # Convenience commands
├── docker-compose.yml        # Docker services orchestration
├── SETUP.md                  # This file
└── backend/                  # FastAPI backend service
    ├── app/                  # Application code
    │   ├── main.py          # FastAPI application entry point
    │   ├── api/             # API route handlers
    │   │   ├── health.py    # Health check endpoints
    │   │   └── accounts.py  # Account management CRUD
    │   ├── core/
    │   │   └── config.py    # Pydantic Settings configuration
    │   ├── database/
    │   │   └── engine.py    # SQLAlchemy ORM setup
    │   ├── models/          # SQLAlchemy ORM models
    │   │   ├── account.py
    │   │   ├── technician.py
    │   │   ├── job.py
    │   │   └── invoice.py
    │   └── schemas/         # Pydantic validation schemas
    │       ├── account.py
    │       ├── technician.py
    │       ├── job.py
    │       ├── invoice.py
    │       └── health.py
    ├── migrations/          # Alembic database migrations
    │   ├── env.py
    │   ├── script.py.mako
    │   └── versions/
    │       └── 001_initial_schema.py
    ├── pyproject.toml       # Poetry project configuration
    ├── Dockerfile           # Docker container definition
    ├── .dockerignore        # Docker build ignore rules
    ├── alembic.ini          # Alembic configuration
    ├── .env.example         # Backend environment template
    └── README.md            # Backend documentation
```

## Prerequisites

- **Docker** 20.10+
- **Docker Compose** 1.29+
- **Python** 3.11+ (for local development only)
- **Poetry** (for local development only)

## Quick Start

### 1. Setup Environment

Create your `.env` file from the template:

```bash
cp .env.example .env
```

Update the required settings in `.env`:

```env
# Required: Your FSM API key
FSM_API_KEY=your_actual_fsm_api_key_here

# Optional: Your LLM API key (if using AI features)
LLM_API_KEY=your_llm_api_key_here
```

### 2. Build and Run with Docker

Start all services (PostgreSQL + FastAPI backend):

```bash
docker compose up --build
```

Or use the Makefile:

```bash
make dev
```

The backend will:
- Wait for PostgreSQL to be healthy
- Automatically apply all database migrations
- Start on port 8000

### 3. Access the API

Once running, visit:

- **Root endpoint**: http://localhost:8000
- **OpenAPI Swagger UI**: http://localhost:8000/api/docs
- **ReDoc documentation**: http://localhost:8000/api/redoc
- **OpenAPI JSON schema**: http://localhost:8000/api/openapi.json

### 4. Test Health Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Readiness check (validates DB connectivity)
curl http://localhost:8000/readiness
```

## Local Development Setup

### 1. Install Dependencies

```bash
cd backend
poetry install
```

### 2. Create Environment File

```bash
cp .env.example .env
```

Configure your PostgreSQL connection and API keys in `.env`.

### 3. Start PostgreSQL

Option A: Using Docker

```bash
docker run --name field-solutions-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=field_solutions \
  -p 5432:5432 \
  -d postgres:16-alpine
```

Option B: Using an existing PostgreSQL server

Update the `DATABASE_URL` in `.env` to point to your server.

### 4. Run Migrations

```bash
poetry run alembic upgrade head
```

### 5. Start Development Server

```bash
poetry run uvicorn app.main:app --reload
```

The server will watch for file changes and auto-reload.

## Common Commands

### Docker Compose

```bash
# Start services
docker compose up

# Start in background
docker compose up -d

# Stop services
docker compose down

# Remove volumes (cleans database)
docker compose down -v

# View logs
docker compose logs -f

# View backend logs only
docker compose logs -f backend

# View database logs only
docker compose logs -f postgres

# Execute command in backend container
docker compose exec backend bash
```

### Makefile Commands

```bash
# View all available commands
make help

# Build Docker images
make build

# Start services
make up

# Stop services
make down

# View logs
make logs

# View backend logs
make logs-backend

# View database logs
make logs-db

# Run migrations
make migrate

# Start in dev mode with build
make dev

# Clean containers and volumes
make clean
```

### Database Migrations

```bash
# Apply all pending migrations
poetry run alembic upgrade head

# Create a new migration
poetry run alembic revision --autogenerate -m "Add new table"

# View migration history
poetry run alembic history

# View current migration version
poetry run alembic current

# Rollback one migration
poetry run alembic downgrade -1

# Rollback to a specific revision
poetry run alembic downgrade <revision_id>
```

## Environment Variables

### Required Settings

```env
# Database connection URL (PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/dbname

# FSM API configuration
FSM_API_KEY=your_fsm_api_key_here
```

### Optional Settings

```env
# FSM API URL (defaults to https://api.fieldsolutionsmanager.com)
FSM_API_URL=https://api.fieldsolutionsmanager.com

# LLM API key for AI features (optional)
LLM_API_KEY=your_llm_api_key_here

# Application settings
APP_NAME=Field Solutions Backend
DEBUG=false
DATABASE_ECHO=false

# Docker Compose settings
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=field_solutions
DB_PORT=5432
BACKEND_PORT=8000
```

## Database Schema

The initial migration creates four main tables:

### Accounts

Stores customer/organization account information:
- id (primary key)
- name, email (unique), phone, address, city, state, zip_code
- is_active, created_at, updated_at

### Technicians

Service technicians associated with accounts:
- id (primary key)
- account_id (foreign key to accounts)
- first_name, last_name, email (unique), phone
- specialization, license_number
- is_active, created_at, updated_at

### Jobs

Service jobs/tickets:
- id (primary key)
- account_id, technician_id (foreign keys)
- title, description
- address, city, state, zip_code
- status (enum: pending, in_progress, completed, cancelled)
- scheduled_date, completed_date
- created_at, updated_at

### Invoices

Job invoices:
- id (primary key)
- account_id, job_id (foreign keys)
- invoice_number (unique), description
- amount, tax_amount, total_amount
- status (enum: draft, sent, paid, overdue, cancelled)
- issued_date, due_date, paid_date, notes
- created_at, updated_at

## API Endpoints

### Health Checks

- `GET /health` - Application health status
- `GET /readiness` - Database connectivity check

### Accounts (with full CRUD)

- `POST /api/accounts` - Create account
- `GET /api/accounts` - List accounts (with pagination)
- `GET /api/accounts/{id}` - Get account by ID
- `PATCH /api/accounts/{id}` - Update account
- `DELETE /api/accounts/{id}` - Delete account

## Features Implemented

✅ **FastAPI** with Python 3.11
✅ **Poetry** dependency management
✅ **Docker** containerization with Dockerfile
✅ **Docker Compose** for local PostgreSQL + backend
✅ **Pydantic Settings** for configuration management
✅ **SQLAlchemy ORM** with Alembic migrations
✅ **Health/Readiness** endpoints
✅ **Shared schemas** for accounts, technicians, jobs, invoices
✅ **OpenAPI documentation** at `/api/docs`
✅ **CORS middleware** enabled
✅ **Environment variable** configuration
✅ **Automatic migration** execution on startup

## Troubleshooting

### Port Already in Use

If port 8000 or 5432 is already in use:

```bash
# Check what's using the port
lsof -i :8000
lsof -i :5432

# Change ports in .env or docker-compose.yml
# For docker-compose, update the ports section
```

### Database Connection Error

```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Check PostgreSQL logs
docker compose logs postgres

# Verify DATABASE_URL in .env is correct
# Format: postgresql://user:password@host:port/dbname
```

### Migration Failures

```bash
# View migration history
docker compose exec backend alembic history

# Check current migration version
docker compose exec backend alembic current

# Check alembic.ini is correctly configured
# Ensure app.database.engine.Base is imported in env.py
```

### Container Build Issues

```bash
# Rebuild from scratch
docker compose build --no-cache

# Check Dockerfile syntax
docker build -f backend/Dockerfile --dry-run .
```

## Testing

### Run Tests

```bash
poetry run pytest
```

### Test with Coverage

```bash
poetry run pytest --cov=app --cov-report=html
```

## Development Best Practices

1. **Database Changes**: Create migrations for all schema changes
2. **Code Style**: Follow PEP 8 conventions
3. **Type Hints**: Use Python type hints for better IDE support
4. **Docstrings**: Add docstrings to functions and classes
5. **Environment Secrets**: Never commit `.env` files, use `.env.example` as template
6. **Testing**: Write tests for new endpoints and functionality

## Next Steps

1. Implement additional API endpoints (technicians, jobs, invoices)
2. Add authentication/authorization
3. Add comprehensive error handling
4. Add request/response logging
5. Add data validation rules
6. Add unit and integration tests
7. Add API rate limiting
8. Add database connection pooling configuration

## Support

For issues or questions about the backend setup, refer to:

- `backend/README.md` - Backend-specific documentation
- `docker-compose.yml` - Service configuration
- `.env.example` - Environment variables reference
- Alembic documentation: https://alembic.sqlalchemy.org/

---

**Last Updated**: 2024
**Backend Version**: 0.1.0
**Python Version**: 3.11+
