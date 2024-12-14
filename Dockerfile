# Use an official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (including libpq-dev for PostgreSQL)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

RUN pip install --upgrade pip

# Copy the application files
COPY . .

# Install dependencies
RUN pip install flask flask-sqlalchemy psycopg2

# Expose the port Flask runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]