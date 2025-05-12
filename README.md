git clone https://github.com/<AnaBaramashvili>/mindcare.git
cd mindcare
cp .env.example .env    # fill in real values
docker-compose up --build -d
docker-compose exec web flask db upgrade
