# Railway Management System API

A RESTful backend system for managing railway operations including train schedules, station information, and seat booking functionality.

## Core Features

- JWT-based authentication with role segregation (Admin/User)
- PostgreSQL database integration
- Admin operations with API key protection
- Race condition handling for concurrent booking attempts
- Comprehensive API for railway operations management

## Tech Stack

- Django 4.2.4
- Django REST Framework 3.14.0
- PostgreSQL
- JWT Authentication (Simple JWT)
- Django REST Framework docs

## Development Setup

### System Requirements

- Python 3.8+
- PostgreSQL 12+
- Git

### Local Setup

1. Clone the repository
```bash
git clone https://github.com/your-username/railway-management-api.git
cd railway-management-api
```

2. Set up virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Database Configuration
   - Create PostgreSQL database
   ```sql
   CREATE DATABASE railway_db;
   ```
   - Configure database settings in `irctc_api/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'railway_db',
           'USER': 'postgres',
           'PASSWORD': 'your-db-password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. Apply database migrations
```bash
python manage.py migrate
```

6. Create admin user
```bash
python manage.py createsuperuser
```

7. Start development server
```bash
python manage.py runserver
```

## API Reference

### Authentication Endpoints

| Endpoint | Method | Description | Request Body |
|----------|--------|-------------|-------------|
| `/api/users/register/` | POST | Register new user | `{"email": "user@example.com", "username": "user1", "password": "password123"}` |
| `/api/users/login/` | POST | User login | `{"email": "user@example.com", "password": "password123"}` |
| `/api/users/token/refresh/` | POST | Refresh access token | `{"refresh": "<refresh_token>"}` |

### Admin Endpoints

All admin endpoints require:
- Header: `Authorization: Bearer <access_token>`
- Header: `X-API-KEY: railway_management_admin_api_key`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/railway/admin/stations/` | GET/POST | Get all or create station |
| `/api/railway/admin/trains/` | GET/POST | Get all or create train |
| `/api/railway/admin/routes/` | GET/POST | Get all or create route |

### User Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|---------------|
| `/api/railway/availability/?source=1&destination=2` | GET | Check train availability | Not required |
| `/api/railway/book/` | POST | Book a seat | Required |
| `/api/railway/bookings/` | GET | List user bookings | Required |
| `/api/railway/bookings/<uuid>/` | GET | Get booking details | Required |

## Concurrency Handling

The booking system implements database-level locking using Django's `select_for_update()` to prevent race conditions during concurrent booking attempts. The transaction isolation ensures that:

1. Seat availability is checked within a transaction
2. Row-level locking prevents parallel updates to the same route
3. Available seats are decremented atomically

Implementation:
```python
with transaction.atomic():
    route = Route.objects.select_for_update().get(id=route_id)
    # Booking logic and seat allocation
```

## API Documentation

Interactive API documentation is available at `/docs/` when the server is running.

## Testing

To run the test suite:
```bash
python manage.py test
```

## Security Considerations

- API keys for admin endpoints should be stored in environment variables in production
- JWT tokens have a configurable expiry (default: access=1h, refresh=1d)
- User passwords are hashed using Django's default PBKDF2 algorithm
- Database connections use TLS in production environment
