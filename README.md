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

## Features
- User registration and authentication (JWT)
- Project and contributor management
- Issue tracking with assignment and status management
- Commenting system
- Role-based permissions (admin/contributor/author)

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
  
4. Run the development server:
```bash
poetry run python manage.py runserver
```

5. The API will be available at:  
http://127.0.0.1:8000/

## Postman collection
A Postman collection is provided to help you test the API quickly.  

### Files
- `docs/postman/OC_P10-SoftDesk_API.postman_collection.json`
- `docs/postman/OC_P10-Softdesk_API.postman_environment.example.json`

### Import
1. Open Postman
2. Click **Import**
3. Import the collection JSON file
4. Import the environment example JSON file

### Authentication
This API uses JWT authentication.

1. Run `POST /api/auth/token/` to obtain tokens
2. Tokens are automatically stored in `access_token` and `refresh_token` in the environment
3. Authenticated requests use `Authorization: Bearer {{access_token}}`
4. When the token expires, run `POST /api/auth/token/refresh/` to refresh it

## Notes
- This app is designed for educational purposes only.
- This project is API only (no frontend included).

## Author
Anselmlys
