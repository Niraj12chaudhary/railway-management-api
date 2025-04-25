# Railway Management System API (IRCTC-like)

This is a RESTful API for a railway management system similar to IRCTC, where users can check train availability between stations and book seats.

## Features

- User Registration and Authentication with JWT tokens
- Role-based access control (Admin and Regular User roles)
- Admin endpoints for managing trains, stations, and routes (protected by API key)
- Check train availability between source and destination
- Book seats with race condition handling
- View booking details and user bookings

## Technology Stack

- **Framework**: Django / Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Django REST framework docs

## Project Setup

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. Clone the repository
```
git clone <repository-url>
cd railway-management-api
```

2. Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Database Setup
   - Create a PostgreSQL database named `railway_db`
   - Update database credentials in `settings.py` if needed
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'railway_db',
           'USER': 'postgres',  # Change if needed
           'PASSWORD': 'postgres',  # Change if needed
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. Run migrations
```
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser (this will be your admin)
```
python manage.py createsuperuser
```
   - When prompted, provide email, username, and password
   - The system will automatically set the role to 'ADMIN' for superusers

7. Start the development server
```
python manage.py runserver
```

## API Endpoints

### Authentication

- **Register User**: `POST /api/users/register/`
  - Request: `{ "username": "user1", "email": "user@example.com", "password": "password", "password_confirm": "password", "first_name": "First", "last_name": "Last" }`
  - Response: User details with JWT tokens

- **Login User**: `POST /api/users/login/`
  - Request: `{ "email": "user@example.com", "password": "password" }`
  - Response: User details with JWT tokens

- **Refresh Token**: `POST /api/users/token/refresh/`
  - Request: `{ "refresh": "<refresh_token>" }`
  - Response: New access token

### Admin Endpoints (Protected by API Key)

All admin endpoints require:
- Authorization header: `Bearer <access_token>`
- X-API-KEY header: `railway_management_admin_api_key`

- **Add/List Stations**: `POST/GET /api/railway/admin/stations/`
  - Add: `{ "name": "New Delhi", "code": "NDLS", "city": "Delhi" }`

- **Add/List Trains**: `POST/GET /api/railway/admin/trains/`
  - Add: `{ "name": "Rajdhani Express", "train_number": "12301", "total_seats": 500 }`

- **Add/List Routes**: `POST/GET /api/railway/admin/routes/`
  - Add: `{ "train": 1, "source": 1, "destination": 2, "departure_time": "2023-08-15T10:00:00Z", "arrival_time": "2023-08-15T18:00:00Z" }`

### User Endpoints

- **Check Train Availability**: `GET /api/railway/availability/?source=1&destination=2`
  - Response: List of available trains with seat counts

- **Book a Seat**: `POST /api/railway/book/` (requires authentication)
  - Request: `{ "route_id": 1 }`
  - Response: Booking details

- **View Booking Details**: `GET /api/railway/bookings/<booking_id>/` (requires authentication)
  - Response: Detailed booking information

- **View User Bookings**: `GET /api/railway/bookings/` (requires authentication)
  - Response: List of user's bookings

## Race Condition Handling

The seat booking system uses database transactions with row-level locking (`select_for_update`) to handle race conditions when multiple users attempt to book seats simultaneously. This ensures that only one booking operation can modify the seat availability data at a time, preventing overbooking.

## API Documentation

API documentation is available at `/docs/` endpoint when the server is running.

## Security

- JWT authentication ensures secure access to protected endpoints
- Admin endpoints are protected by both JWT and API key
- API keys should be stored as environment variables in production
- Password validation ensures strong user passwords
