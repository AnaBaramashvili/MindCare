from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import User, BMI, HealthLog  
from app.forms import HealthLogForm
from utils.health import calculate_health_score

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/manage')


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("Admins only!", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/users')
@login_required
@admin_required
def user_list():
    users = User.query.all()
    bmis = {b.user_id: b for b in BMI.query.all()}
    return render_template('admin/user_list.html', users=users, bmis=bmis)


@admin_bp.route('/users/view/<int:user_id>')
@login_required
@admin_required
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    bmi = BMI.query.filter_by(user_id=user.id).first()
    logs = HealthLog.query.filter_by(user_id=user.id).order_by(HealthLog.date.desc()).all()

    return render_template('admin/view_user.html', user=user, bmi=bmi, logs=logs)


@admin_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    bmi = BMI.query.filter_by(user_id=user.id).first()
    logs = HealthLog.query.filter_by(user_id=user.id).order_by(HealthLog.date.desc()).all()
    form = HealthLogForm()

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role = request.form['role']

        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password or confirm_password:
            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return render_template('admin/edit_user.html', user=user, bmi=bmi, logs=logs, form=form)
            if password:
                user.set_password(password)

        db.session.commit()

        if bmi:
            bmi.age = request.form['age']
            bmi.gender = request.form['gender']
            bmi.height = request.form['height']
            bmi.weight = request.form['weight']
        else:
            bmi = BMI(
                user_id=user.id,
                age=request.form['age'],
                gender=request.form['gender'],
                height=request.form['height'],
                weight=request.form['weight']
            )
            db.session.add(bmi)

        db.session.commit()
        return redirect(url_for('admin_bp.user_list'))

    return render_template('admin/edit_user.html', user=user, bmi=bmi, logs=logs, form=form)

@admin_bp.route('/users/<int:user_id>/logs/<int:log_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_log(user_id, log_id):
    log = HealthLog.query.get_or_404(log_id)
    form = HealthLogForm(obj=log)
    

    if form.validate_on_submit():
        log.sleep_hours = form.sleep_hours.data
        log.exercise_minutes = form.exercise_minutes.data
        bmi = BMI.query.filter_by(user_id=user_id).first()
        log.health_score = calculate_health_score(
            log.sleep_hours, log.exercise_minutes,
            bmi.weight, bmi.height, bmi.age, bmi.gender
        )
        db.session.commit()

        return redirect(url_for('admin_bp.edit_user', user_id=user_id))

    return render_template('admin/edit_log.html', form=form, user_id=user_id)


@admin_bp.route('/users/<int:user_id>/logs/<int:log_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_log(user_id, log_id):
    log = HealthLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    
    return redirect(url_for('admin_bp.edit_user', user_id=user_id))



@admin_bp.route('/users/<int:user_id>/logs/add', methods=['POST'])
@login_required
@admin_required
def add_log(user_id):
    form = HealthLogForm()
    if form.validate_on_submit():
        bmi = BMI.query.filter_by(user_id=user_id).first()
        health_score = calculate_health_score(
            form.sleep_hours.data,
            form.exercise_minutes.data,
            bmi.weight, bmi.height, bmi.age, bmi.gender
        )
        new_log = HealthLog(
            user_id=user_id,
            date=form.date.data,
            sleep_hours=form.sleep_hours.data,
            exercise_minutes=form.exercise_minutes.data,
            health_score=health_score
        )
        db.session.add(new_log)
        db.session.commit()
       
    else:
        flash("Failed to add log. Please check the data.", "danger")
    return redirect(url_for('admin_bp.edit_user', user_id=user_id))


@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    bmi = BMI.query.filter_by(user_id=user.id).first()
    if bmi:
        db.session.delete(bmi)
    db.session.delete(user)
    db.session.commit()
    
    return redirect(url_for('admin_bp.user_list'))
