# Project Overview

This is a multi-tenant SaaS (Software as a Service) application built with Django, designed for managing clubs. Each club operates as an isolated tenant with its own members, financial records (fees and payments), and administrative users. The application leverages Django REST Framework for API capabilities and uses PostgreSQL as its primary database.

**Key Features:**

*   **Multi-Tenancy:** Clubs are isolated by a unique subdomain slug in the URL (e.g., `/hockeyracing/`).
*   **User Management:** Custom user model with role-based access control (`ADMIN`, `TREASURER`, etc.) per club.
*   **Member Management:** CRUD operations for club members, including auto-generated incremental member numbers.
*   **Fee & Payment Management:** Functionality to generate fees for members and record payments.
*   **Dockerized Environment:** The entire application stack (web, database, pgAdmin) is containerized using Docker Compose.

**Core Technologies:**

*   **Backend:** Django, Django REST Framework
*   **Database:** PostgreSQL
*   **Web Server:** Gunicorn
*   **Static Files:** Whitenoise
*   **Containerization:** Docker, Docker Compose

## Building and Running

This project is designed to be run using Docker Compose. Ensure you have Docker and Docker Compose installed on your system.

1.  **Environment Variables:** Create a `.env` file in the project root based on `docker-compose.yml` and your database configuration. You will need to define at least:
    *   `SECRET_KEY`
    *   `DEBUG`
    *   `ALLOWED_HOSTS`
    *   `POSTGRES_DB`
    *   `POSTGRES_USER`
    *   `POSTGRES_PASSWORD`
    *   `DATABASE_HOST`
    *   `DATABASE_PORT`
    *   `DATABASE_NAME`
    *   `PGADMIN_DEFAULT_EMAIL`
    *   `PGADMIN_DEFAULT_PASSWORD`

2.  **Build and Run Services:**
    Navigate to the project root directory in your terminal and run:
    ```bash
    docker compose up -d --build
    ```
    This command will build the Docker images, create the containers, and start all services (web, db, pgadmin) in detached mode.

3.  **Apply Database Migrations:**
    The `entrypoint.sh` script automatically applies migrations on container startup. However, if you make changes to models after the initial setup, you'll need to create and apply new migrations:
    ```bash
    docker compose exec web python manage.py makemigrations core
    docker compose exec web python manage.py migrate
    ```

4.  **Access the Application:**
    Once the services are up and running, you can access the application in your web browser:
    *   **Django Application:** `http://localhost:8000/` (or `http://localhost:8000/<your_club_slug>/`)
    *   **pgAdmin:** `http://localhost:5050/`

5.  **Restarting the Web Service:**
    If you make code changes, you can restart just the web service to apply them:
    ```bash
    docker compose restart web
    ```
    If you've changed dependencies or the `Dockerfile`, you might need to rebuild:
    ```bash
    docker compose up -d --build web
    ```

## Development Conventions

*   **Code Formatting:** The project uses `black` for code formatting. It's recommended to run `black .` before committing changes.
*   **Linting:** `flake8` is used for linting to enforce code style and catch potential errors.
*   **Testing:** `pytest-django` is included for writing and running tests. Tests are located in `tests.py` files within each app.
*   **Multi-Tenancy:** The application implements multi-tenancy via a custom `ClubMiddleware` and URL routing based on a `club_slug`.
*   **Custom User Model:** A `CustomUser` model is used, extending Django's `AbstractUser`.
*   **Model `save()` Overrides:** Custom logic for fields like `member_number` is handled directly in the `form_valid` method of the views for explicit control, rather than overriding the model's `save()` method.
