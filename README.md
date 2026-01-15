# OC Project 10: Softdesk API

This project is carried out as part of the OpenClassrooms training program. 
Softdesk is a RESTful API built with Django and Django REST Framework. It provides a backend service for managing projects, contributors, issues, and comments.

## Tech stack
- Python 3.10
- Django
- Django REST framework
- JWT Authentication (SimpleJWT)
- Poetry (dependency management)

## Prerequisites
Make sure you have the following installed:
- Python 3.10
- Poetry
- Git

## Installation
1. Clone the repository:
```bash
git clone https://github.com/anselmlys/OC_P10_SoftDesk
cd OC_P10_SoftDesk
```

2. Install dependencies with Poetry:
```bash
poetry install
```

3. Apply migrations:
```bash
poetry run python manage.py migrate
```
  
5. Run the development server:
```bash
poetry run python manage.py runserver
```

6. The API will be available at:  
http://127.0.0.1:8000/

## Authentication
This API uses JWT authentication.

## Notes
- This app is designed for educational purposes only.
- This project is API only (no frontend included).

## Author
Anselmlys
