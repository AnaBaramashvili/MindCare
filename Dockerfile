# 1. Pick a small, official Python image as our base
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install any OS-level libraries (e.g., libpq-dev for PostgreSQL)
RUN apt-get update \
  && apt-get install -y build-essential libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# 4. Copy only requirements first (layers cache nicely)
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your application code
COPY . .

# 7. Tell Docker which port your app listens on
EXPOSE 5000

# 8. Set environment variables inside the container
ENV FLASK_ENV=production

# 9. Define the default command to run your app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
