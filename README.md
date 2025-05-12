# 1. Clone the repo
git clone https://github.com/AnaBaramashvili/mindcare.git
cd mindcare

# 2. Copy and fill in your environment variables
cp .env.example .env
# └─ edit .env and set SECRET_KEY, POSTGRES_PASSWORD, etc.

# 3. Build & start the containers
docker-compose up --build -d

# 4. Run database migrations
docker-compose exec web flask db upgrade

# 5. Visit the app
open http://localhost:5000
