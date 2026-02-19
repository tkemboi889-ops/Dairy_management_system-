# Dairy Management Information System API

A Django REST Framework (DRF) API for managing dairy farm operations including livestock, milk production, feed, and workers.  
The system supports secure authentication.

## Features
- User authentication (login, logout, registration)
- Token-based authentication
- Livestock (cows & calves) management
- Milk production records
- Feed and worker management
- RESTful API endpoints

## Tech Stack
- Django & Django REST Framework
- MySQL
- DRF Token Authentication
- Git & GitHub
- Postman (API testing)
- python 3.13
- Gunicorn
- render(deployment)

## Setup
```bash
git clone https://github.com/tkemboi889-ops/dairy-management-system-api.git
cd dairy-management-system-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

## ⚙️ Installation Guide

### 1. Clone the Repository

git clone https://github.com/tkemboi889-ops/dairy-management-system.git

### 2. Create Virtual Environment

python -m venv venv

### 3. Activate Virtual Environment

source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

### 4. Install Dependencies

pip install -r requirements.txt

### 5. Run Migrations

python manage.py migrate

### 6. Run Server

python manage.py runserver

##  Environment Variables

Create a .env file and add:

SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url

##  API Endpoints

###  Authentication

POST /api/auth/register/
POST /api/auth/login/

### 🥛 Milk Records

GET /api/milk/
POST /api/milk/

### calves

GET /api/calves/
POST /api/calves/
### workers
GET /api/workers/
POST /api/workers/

##  Authentication

This API uses JWT Authentication.

After login, you will receive:

- access token
- refresh token

Use the access token in headers:

Authorization: Bearer your_access_token

##  Deployment

The API is deployed on Render:

https://dairy-management-system-q1z3.onrender.com/

##  Author

Timothy Kemboi
Backend Developer










