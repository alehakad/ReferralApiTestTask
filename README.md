# Referral System API

This is a RESTful API service for managing a referral system. It enables user registration, authentication, referral code management, and tracking of referred users. Built with FastAPI and SQLAlchemy.

## Features

- **User Registration and Authentication** using JWT or OAuth 2.0
- **Referral Code Management**: create, retrieve, and delete referral codes with expiration settings
- **Referral Tracking**: register users via referral code and track referrals by referrer
- **API Documentation** with Swagger/ReDoc

## Project Structure

```plaintext
project_root/
├── app/
│   ├── main.py                # Application entry point
│   ├── dependencies.py        # Dependencies: JWT validation: getting current user
│   ├── schemas/               # Pydantic models for request/response validation
│   ├── models/                # Database ORM models
│   ├── routers/               # API endpoint routes
│   ├── utils/                 # Utility functions for JWT
│   └── db.py                  # Database connection and setup
├── tests/                     # Pytest examples
├── .env                       # Environment variables (DB URL, JWT secret, etc.)
├── Dockerfile                 # Dockerfile of application
├── docker-compose.yml         # Docker Compose with Postrgres and FastAPI containers
├── README.md                  # Project overview and setup instructions
└── requirements.txt           # Python dependencies to install
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
   or manually 
    ```bash
    pip install -r requirements.txt
    uvicorn app.main:app --reload
    ```
   
4. **Access the API** at ```bash http://localhost:8000```

5. **To run tests** ```bash pytest``` in main project directory
