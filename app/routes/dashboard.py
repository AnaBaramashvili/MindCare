from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user
from app.forms import HealthLogForm
from app.services.health import HealthService
from datetime import datetime
from app.extensions import db

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = HealthLogForm()
    user = current_user
    stats = HealthService.weekly_stats(user)
    if not stats or not stats['bmi_record']:
        if user.role == "admin":
            return redirect(url_for('admin_bp.user_list'))
        else:
            flash("BMI record not found. Please complete your profile.", "danger")
            return redirect(url_for('user_bp.profile'))
    if form.validate_on_submit():
        log, error = HealthService.submit_log(user, form.sleep_hours.data, form.exercise_minutes.data)
        if error:
            flash(error, 'warning')
            return redirect(url_for('dashboard_bp.dashboard'))
        if log:
            db.session.commit()
        flash('Health data logged successfully!', 'success')
        return redirect(url_for('dashboard_bp.dashboard'))
    alerts = HealthService.check_alerts(stats)
    show_welcome = session.pop('show_welcome', False)
    today = datetime.utcnow().date()
    return render_template("user/dashboard.html",
        form=form,
        bmi=round(stats['bmi_record'].weight / ((stats['bmi_record'].height / 100) ** 2), 2) if stats['bmi_record'].height > 0 else None,
        bmi_record=stats['bmi_record'],
        logs=stats['logs'],
        avg_sleep=round(alerts['avg_sleep'], 1),
        exercise_days=alerts['exercise_days'],
        alert_exercise=alerts['alert_exercise'],
        alert_sleep=alerts['alert_sleep'],
        date=today,
        formatted_dates=stats['formatted_dates'],
        health_scores=stats['health_scores'],
        show_welcome=show_welcome
    ) 