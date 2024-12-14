# Use an official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install flask flask-sqlalchemy psycopg2 random

# Expose the port Flask runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]