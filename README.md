# PDS Services API

A RESTful API built with **FastAPI** and **Python** for managing services, training programmes, users and orders — developed as a university team project.

## What it does

A backend platform for managing a services and training business, including user authentication, role-based access control, service/training catalogue management, and order processing.

## Features

- **JWT Authentication** — secure token-based login and session management
- **Role-based access** — Admin, Manager, Owner and User roles with granular permissions
- **User management** — registration, profile management, address and contact handling
- **Services** — create, list and manage service offerings
- **Training** — training programmes with categories and plans
- **Orders** — order creation and tracking linked to services
- **Companies** — company and owner management
- **Database migrations** — Alembic-managed schema versioning

## Tech Stack

- **FastAPI** — modern, high-performance Python web framework
- **SQLAlchemy** — ORM for database interaction
- **Alembic** — database migrations
- **MySQL** (PyMySQL) — relational database
- **JWT** (python-jose) — token-based authentication
- **bcrypt / passlib** — secure password hashing
- **Pydantic** — data validation and serialisation
- **Uvicorn** — ASGI server

## Architecture

```text
app/
├── api/
│   ├── handlers/        # Route handlers (auth, user, owner, service, training, order)
│   ├── schemas/         # Pydantic DTOs (request/response models)
│   └── service/         # Business logic layer
├── core/
│   ├── auth.py          # JWT creation and validation
│   ├── config.py        # App configuration
│   └── utils.py         # Shared utilities
├── database/
│   ├── models/          # SQLAlchemy ORM models
│   └── repository.py    # Generic database repository
└── main.py              # App entry point, middleware config
alembic/                 # Database migration scripts
scripts/                 # SQL seed scripts (roles, permissions, categories)
```

## Data Models

- `User` — application users with roles and permissions
- `Owner` — business owners linked to companies
- `Company` — company entities with addresses
- `Service` — service offerings with categories and pricing
- `Training` — training programmes with plans and categories
- `Order` — orders linking users to services
- `Address` / `Contact` — supporting entities

## How to Run

### Prerequisites

- Python 3.10+
- MySQL database
- Pipenv

### Setup

```bash
# Install dependencies
pipenv install

# Activate virtual environment
pipenv shell

# Configure database connection
# Edit settings.json with your MySQL host, user, password and database

# Run database migrations
alembic upgrade head

# Seed initial data
mysql -u your_user -p your_db < scripts/insert_role.sql
mysql -u your_user -p your_db < scripts/insert_permission.sql

# Start the server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

Interactive docs at `http://localhost:8000/docs`

## API Endpoints

| Method | Endpoint        | Description                   |
|--------|-----------------|-------------------------------|
| POST   | `/auth/login`   | Login and receive JWT token   |
| POST   | `/user/`        | Register new user             |
| GET    | `/user/`        | List users (admin)            |
| GET    | `/owner/`       | List owners                   |
| POST   | `/service/`     | Create service                |
| GET    | `/service/`     | List services                 |
| POST   | `/training/`    | Create training               |
| GET    | `/training/`    | List training programmes      |
| POST   | `/order/`       | Create order                  |

## Concepts Demonstrated

- **FastAPI** with dependency injection and async routing
- **SQLAlchemy ORM** with relationship mapping
- **Alembic** schema migrations
- **JWT** authentication with role-based route protection
- **Pydantic** DTO pattern for clean API contracts
- **Layered architecture** — handlers → services → repository → models
