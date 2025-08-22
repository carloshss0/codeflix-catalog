# Codeflix Catalog

A python microservice for managing catalog, following clean architecture principles.

## Project Structure

- domain: Domain models and business logic.
- application: Application services and use cases.
- infrastructure: Infrastructure implementations (e.g., in-memory repositories, MySQL repository).
- tests: Unit and integration tests.

## Features

- Create (categories and genres).
- Get (categories and genres).
- Update (categories and genres).
- Delete (categories and genres).
- List (categories and genres).
- In-memory repository for testing and development.
- SQL lite repository for testing and development (Django ORM).
- Separation of domain, application, and infrastructure layers.
- API endpoints: GET (specific category), GET (all), CREATE, PUT (update all fields), PATCH (update specifics fields), DELETE

## Getting Started

1. **Create virtual env**
   ```
   python3 -m venv venv (macos | linux)
   python -m venv venv (Windows)
   ````

2. **Activate virtual env**
   ```
   source venv/bin/activate (macos | linux)
   .\venv/Scripts\activate (Windows)


3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests**  
   ```bash
   pytest src/core/category/tests/
   ```
5. **Start server**
   ```bash
   python manage.py runserver
   ```