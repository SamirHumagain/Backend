# Venue Reservation System - Backend

A Django REST Framework API for managing venues, reservations, events, and user accounts for a venue reservation platform.

## Overview

This backend provides RESTful APIs for:

- **Venue Management**: Create, update, and manage venue details, services, and images
- **Event Planning**: Manage event types and booking workflows
- **User Management**: Handle user authentication, authorization, and user profiles
- **Reservations**: Book venues and manage reservation statuses
- **Ratings & Reviews**: Submit and retrieve venue ratings
- **Payments**: Khalti payment integration for secure transactions

## Tech Stack

- **Framework**: Django + Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: Token-based authentication
- **Payment Gateway**: Khalti

## Project Structure

```
Backend/
├── manage.py                 # Django management entry point
├── requirements.txt          # Python dependencies
├── VenueReservation/         # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── venues/                   # Venue and service management
├── eventplanner/             # Event type and planning
├── loginsignup/              # User authentication and signup
├── khalti/                   # Payment integration
├── rating/                   # Venue ratings and reviews
└── media/                    # User uploads (images, profiles)
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd Backend
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**

   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`

## API Documentation

### Key Endpoints

- **Venues**: `/api/venues/` - List, create, and manage venues
- **Services**: `/api/services/` - Manage venue services
- **Reservations**: `/api/reservations/` - Book and manage reservations
- **Events**: `/api/events/` - Create and manage event types
- **Auth**: `/api/auth/` - User authentication
- **Ratings**: `/api/ratings/` - Submit and retrieve ratings

## Testing

Run the test suite:

```bash
python manage.py test
```

## Environment Variables

Create a `.env` file in the Backend folder with:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Database Migrations

After making changes to models:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Contributing

1. Create a new branch for features
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT License - see LICENSE file for details
