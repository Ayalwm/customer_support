# Customer Support Ticketing System

This project is a Customer Support Ticketing System built using Django and SQLite. It runs in a Docker container with a custom network setup.

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/Ayalwm/customer_support.git
cd customer_support
```

### 2. Create a `.env` File

Create a `.env` file in the project root and add the following:

```ini
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_HOST_USER=gcgh.17@gmail.com  # Replace with your actual email
EMAIL_HOST_PASSWORD=gvj  # Replace with your actual app password
DEFAULT_FROM_EMAIL=gcgh.17@gmail.com

DJANGO_SECRET_KEY=your_secret_key

REDIS_URL = sqla+postgresql://postgres:password@db:5432/customer_support
CELERY_URL = db+postgresql://postgres:password@db:5432/customer_support

SITE_URL=http://127.0.0.1:8080
POSTGRES_DB=customer_support
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
DATABASE_URL=postgres://postgres:password@db:5432/customer_support
```

### 3. Build and Start the Containers

```sh
docker-compose up --build -d
```

This will build and start the Django application in a Docker container.

### 4. Access the Application

- The app will be running at: **http://127.0.0.1:8080**
- The Django admin panel is at: **http://127.0.0.1:8080/admin**

This should ensure the system works properly with the required configuration. Let me know if you need any modifications!
