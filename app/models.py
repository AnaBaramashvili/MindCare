from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(20), default='user')

    bmi = db.relationship('BMI', backref='user', uselist=False, cascade="all, delete-orphan")
    health_logs = db.relationship('HealthLog', backref='user', lazy=True, cascade="all, delete-orphan")
    
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class BMI(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    age = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String(10), nullable=False)
    height = db.Column(db.Float, nullable=False)  
    weight = db.Column(db.Float, nullable=False)

class HealthLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    date = db.Column(db.Date, nullable=False)
    sleep_hours = db.Column(db.Float, nullable=False)
    exercise_minutes = db.Column(db.Integer, nullable=False)
    health_score = db.Column(db.Float, nullable=False) 