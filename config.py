import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://mindcareuser:yourpassword@localhost:5432/mindcare'
    SQLALCHEMY_TRACK_MODIFICATIONS = False