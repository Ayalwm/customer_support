# Use a lightweight Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Default command (for running Django server)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "customer_support.wsgi:application"]
