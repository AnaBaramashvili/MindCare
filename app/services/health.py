from datetime import datetime, timedelta
from utils.health import calculate_health_score, calculate_bmi
from app.dal import (
    get_bmi_by_user_id,
    get_log_for_today,
    create_log,
    get_logs_in_range
)

class HealthService:
    @staticmethod
    def submit_log(user, sleep_hours, exercise_minutes):
        bmi_record = get_bmi_by_user_id(user.id)
        if not bmi_record:
            return None, 'BMI record not found.'
        date_val = datetime.utcnow().date()
        existing_log = get_log_for_today(user.id, date_val)
        if existing_log:
            return None, 'Log already exists for today.'
        health_score = calculate_health_score(
            sleep_hours=sleep_hours,
            exercise_minutes=exercise_minutes,
            weight_kg=bmi_record.weight,
            height_cm=bmi_record.height,
            age=bmi_record.age,
            gender=bmi_record.gender
        )
        log = create_log(user.id, date_val, sleep_hours, exercise_minutes, health_score)
        return log, None

    @staticmethod
    def weekly_stats(user):
        bmi_record = get_bmi_by_user_id(user.id)
        if not bmi_record:
            return None
        today = datetime.utcnow().date()
        week_dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
        logs = get_logs_in_range(user.id, week_dates)
        logs_by_date = {log.date: log for log in logs}
        formatted_dates = [d.strftime('%a') for d in week_dates]
        health_scores = []
        for day in week_dates:
            log = logs_by_date.get(day)
            if log:
                score = calculate_health_score(
                    log.sleep_hours, log.exercise_minutes,
                    bmi_record.weight, bmi_record.height,
                    bmi_record.age, bmi_record.gender
                )
            else:
                score = None
            health_scores.append(score)
        return {
            'bmi_record': bmi_record,
            'logs': logs,
            'formatted_dates': formatted_dates,
            'health_scores': health_scores
        }

    @staticmethod
    def check_alerts(stats):
        today = datetime.utcnow().date()
        one_week_ago = today - timedelta(days=7)
        recent_logs = [log for log in stats['logs'] if log.date >= one_week_ago]
        exercise_days = sum(1 for log in recent_logs if log.exercise_minutes > 0)
        avg_sleep = (
            sum(log.sleep_hours for log in recent_logs) / len(recent_logs)
            if recent_logs else 0
        )
        alert_exercise = len(recent_logs) > 0 and exercise_days <= 1
        alert_sleep = len(recent_logs) > 0 and avg_sleep < 6
        return {
            'avg_sleep': avg_sleep,
            'exercise_days': exercise_days,
            'alert_exercise': alert_exercise,
            'alert_sleep': alert_sleep
        } 