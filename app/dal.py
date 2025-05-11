from app.models import User, BMI, HealthLog
from app.extensions import db
from datetime import datetime

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def create_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    return user

def get_bmi_by_user_id(user_id):
    return BMI.query.filter_by(user_id=user_id).first()

def upsert_bmi(user_id, age, gender, height, weight):
    bmi = get_bmi_by_user_id(user_id)
    if not bmi:
        bmi = BMI(user_id=user_id)
        db.session.add(bmi)
    bmi.age, bmi.gender, bmi.height, bmi.weight = age, gender, height, weight
    return bmi

def get_log_for_today(user_id, date):
    return HealthLog.query.filter_by(user_id=user_id, date=date).first()

def create_log(user_id, date, sleep_hours, exercise_minutes, health_score):
    log = HealthLog(
        user_id=user_id,
        date=date,
        sleep_hours=sleep_hours,
        exercise_minutes=exercise_minutes,
        health_score=health_score
    )
    db.session.add(log)
    return log

def get_logs_in_range(user_id, dates):
    return HealthLog.query.filter_by(user_id=user_id).filter(HealthLog.date.in_(dates)).all()

def update_user_profile(user, username, email, bmi, age, gender, height, weight):
    user.username = username
    user.email = email
    if bmi:
        bmi.age = age
        bmi.gender = gender
        bmi.height = height
        bmi.weight = weight
    return user, bmi 