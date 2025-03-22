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

REDIS_URL=redis://redis:6379/0
SITE_URL=http://127.0.0.1:8000
```

### 3. Create a Custom Docker Network (Optional)

```sh
docker network create custom_network
```

### 4. Build and Start the Containers

```sh
docker-compose up --build -d
```

This will build and start the Django application in a Docker container.

### 5. Run Migrations

```sh
docker-compose exec web python manage.py migrate
```

### 6. Create a Superuser (For Admin Access)

```sh
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts to set up an admin account.

### 7. Access the Application

- The app will be running at: **http://127.0.0.1:8000**
- The Django admin panel is at: **http://127.0.0.1:8000/admin**

### 8. Stopping the Containers

To stop the containers, run:

```sh
docker-compose down
```

## Additional Notes

- If you experience any issues with dependencies taking too long, try rebuilding without cache:
  ```sh
  docker-compose build --no-cache
  ```
- If using Gmail for email, you may need to enable **Less Secure Apps** or generate an **App Password** in your Google account settings.

---

This should ensure the system works properly with the required configuration. Let me know if you need any modifications!
