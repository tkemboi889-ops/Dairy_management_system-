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





