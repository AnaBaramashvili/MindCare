# Use an official Python image as the base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP="app:create_app"
ENV FLASK_ENV=production

# Set work directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y gcc

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose the port Flask/Gunicorn runs on
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_RUN_HOST=0.0.0.0

# Run the app with Gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
