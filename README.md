# FastAPI Template Project

A robust FastAPI application template featuring comprehensive request logging, async database operations, and a web-based log viewer. This template provides a solid foundation for building production-ready FastAPI applications with built-in observability.

## Features

- 🔍 Comprehensive API request/response logging
- 📊 Web-based log viewer interface
- 🔄 Async database operations with SQLAlchemy
- ⚡ Fast performance with async I/O
- 🧪 Development tools preconfigured
- 🔒 Type safety with MyPy
- 📝 Code quality tools (Black, Pylint)

## Project Structure

```
fastapi-template/
├── app/
│   ├── core/
│   │   ├── logging/
│   │   │   ├── models.py       # Database models for API logs
│   │   │   ├── middleware.py   # Request logging middleware
│   │   │   └── routes.py       # Log viewer endpoints
│   │   ├── database.py         # Database and Session configuration
│   │   ├── dao.py              # Base Data Access Object (DAO) class
│   │   ├── exceptions.py       # Customized Exception handling
│   │   ├── config.py           # Application configuration
│   │   ├── router.py           # Application route registration
│   │   └── setup.py            # App initialization
│   ├── users/
│   │   ├── models.py           # User-related database models
│   │   ├── schemas.py          # Pydantic models for user data
│   │   ├── routes.py           # User management endpoints
│   │   ├── dao.py              # User DAO
│   │   ├── exceptions.py       # User Exceptions
│   │   └── service.py          # Busines Logic for User management
│   └── templates/
│       └── logs.html           # Log viewer template
├── tests/                      # Functional and Unit tests
├── requirements.txt            # Production dependencies
├── dev-requirements.txt        # Development dependencies
└── run.py                      # Development server entry point
```

The `app/users/` module handles:
- User registration and authentication
- Password hashing and verification
- Role-based access control
- User profile management
- Session handling

## Dependencies

### Production Dependencies
- **FastAPI** (0.115.12): Modern web framework for building APIs
- **SQLAlchemy** (2.0.29): SQL toolkit and ORM
- **aiosqlite** (0.21.0): Async SQLite database driver
- **Jinja2** (3.1.6): Template engine for the log viewer
- **uvicorn** (0.34.0): ASGI server implementation
- **email-validator** (2.2.0): Email validation utility
- **greenlet** (3.1.1): Lightweight in-process concurrent programming
- **dnspython** (2.7.0): DNS toolkit

### Development Dependencies
- **black** (24.4.2): Code formatter
- **pylint** (3.3.4): Code linter
- **mypy** (1.13.0): Static type checker
- **pytest** (8.3.5): Testing framework
- **pytest-asyncio** (0.26.0): Async testing support
- **pytest-cov** (6.0.0): Test coverage reporting
- **httpx** (0.28.1): HTTP client for testing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fastapi-template.git
cd fastapi-template
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/MacOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r dev-requirements.txt  # If developing
```

## Running the Application

Start the development server:
```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`
Log viewer interface: `http://localhost:8000/admin/logs`

## Development

### Code Quality

1. Format code:
```bash
black .
```

2. Run linter:
```bash
pylint app
```

3. Type checking:
```bash
mypy .
```

### Testing

Run tests with coverage:
```bash
pytest --cov=app tests/
```

## API Log Viewer

The template includes a built-in web interface for viewing API logs at `/admin/logs`. Features include:
- Request/response details
- Execution duration
- Status code with color coding
- User ID tracking
- Client IP logging
- Timestamps in EST

## Database

The template uses SQLite by default:
- Development: File-based SQLite database
- Testing: In-memory SQLite database
- Async operations using aiosqlite
- Automatic schema creation on startup

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI documentation
- SQLAlchemy documentation
- Pydantic documentation
