# Backend Service

FastAPI backend service for Field Solutions Management system.

## Prerequisites

- Python 3.11+
- Poetry (dependency management)
- Docker & Docker Compose (for containerized deployment)
- PostgreSQL 16+ (for database)

## Setup

### Local Development

1. Install dependencies with Poetry:
```bash
cd backend
poetry install
```

2. Create a `.env` file in the project root:
```bash
cp ../.env.example .env
```

3. Update `.env` with your configuration:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/field_solutions
FSM_API_KEY=your_api_key_here
```

4. Run migrations:
```bash
poetry run alembic upgrade head
```

5. Start the development server:
```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker Deployment

1. Create a `.env` file in the project root with your configuration

2. Start all services:
```bash
docker compose up
```

The backend will:
- Apply migrations automatically
- Start on port 8000
- Be accessible at `http://localhost:8000`

## API Documentation

Once running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI Schema**: http://localhost:8000/api/openapi.json

## Health Checks

- **Health Check**: `GET /health` - Returns application health status
- **Readiness Check**: `GET /readiness` - Validates database connectivity

## Database Migrations

### Create a new migration:
```bash
poetry run alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations:
```bash
poetry run alembic upgrade head
```

### Rollback to previous migration:
```bash
poetry run alembic downgrade -1
```

## Project Structure

```
backend/
├── app/
│   ├── api/              # API route handlers
│   ├── core/             # Core configuration
│   ├── database/         # Database configuration
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   └── main.py           # FastAPI application entry point
├── migrations/           # Alembic migration files
├── Dockerfile            # Docker configuration
├── pyproject.toml        # Poetry dependencies
└── README.md             # This file
```

## Configuration

Application settings are managed through Pydantic Settings and loaded from environment variables.

Required settings:
- `DATABASE_URL`: PostgreSQL connection string
- `FSM_API_KEY`: Field Solutions Manager API key

Optional settings:
- `FSM_API_URL`: FSM API URL (defaults to https://api.fieldsolutionsmanager.com)
- `LLM_API_KEY`: Optional LLM API key for AI features
- `DEBUG`: Debug mode (defaults to false)

## Schemas

The application includes shared schemas for:

- **Accounts**: Customer/organization accounts
- **Technicians**: Service technicians
- **Jobs**: Service jobs/tickets
- **Invoices**: Job invoices

Each schema includes CRUD operations accessible via REST API.

## Development

### Running Tests

```bash
poetry run pytest
```

### Code Quality

Ensure your code follows the project's style guidelines. Consider using tools like:
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking

## Troubleshooting

### Database Connection Issues

If you see database connection errors:

1. Ensure PostgreSQL is running
2. Verify DATABASE_URL is correct
3. Check that the database user has proper permissions
4. Ensure the database exists

### Migration Issues

If migrations fail:

1. Check the migration file syntax
2. Ensure the database schema is valid
3. Review alembic version history: `alembic history`
4. Check alembic current version: `alembic current`

## License

Part of the Field Solutions Management system.
