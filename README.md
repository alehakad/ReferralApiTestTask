# Referral System API

This is a RESTful API service for managing a referral system. It enables user registration, authentication, referral code management, and tracking of referred users. Built with FastAPI, this project follows best practices for clean, asynchronous code, and offers Swagger UI documentation.

## Features

- **User Registration and Authentication** using JWT or OAuth 2.0
- **Referral Code Management**: create, retrieve, and delete referral codes with expiration settings
- **Referral Tracking**: register users via referral code and track referrals by referrer
- **API Documentation** with Swagger/ReDoc
- **Optional Caching** with in-memory storage for referral codes

## Project Structure

```plaintext
project_root/
├── app/
│   ├── main.py                # Application entry point
│   ├── config.py              # Configuration settings (e.g., database URLs, JWT secrets)
│   ├── dependencies.py        # Dependencies like JWT validation, caching connections
│   ├── schemas/               # Pydantic models for request/response validation
│   ├── models/                # Database ORM models
│   ├── crud/                  # CRUD operations for interacting with the database
│   ├── services/              # Business logic
│   ├── api/                   # API endpoint routes
│   ├── utils/                 # Utility functions for JWT, date handling, etc.
│   └── db.py                  # Database connection and setup
├── tests/                     # Unit and integration tests
├── docs/                      # Swagger/ReDoc documentation setup
├── .env                       # Environment variables (DB URL, JWT secret, etc.)
├── Dockerfile                 # Docker setup for containerization
├── docker-compose.yml         # Docker Compose for services (DB, Redis)
├── README.md                  # Project overview and setup instructions
└── requirements.txt           # Python dependencies
```

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/referral-system-api.git
   cd referral-system-api
   ```
2. **Configure environment variables**:
    - create .env based on .env.example
3. **Build and start the containers**:
    ```bash
    docker-compose up --build
    ```
4. **Access the API** at ```bash http://localhost:8000```
