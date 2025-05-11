from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, current_user
from app.forms import LoginForm, RegistrationForm
from app.dal import get_user_by_email, create_user, upsert_bmi
from app.models import User
from app.extensions import db

auth_bp = Blueprint('auth_bp', __name__)

def handle_login(form):
    if form.validate_on_submit():
        user = get_user_by_email(form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard_bp.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    return None

@auth_bp.route('/')
@auth_bp.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_bp.dashboard'))
    form = LoginForm()
    result = handle_login(form)
    if result:
        return result
    return render_template('auth/index.html', title='Welcome to Mindcare', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_bp.dashboard'))
    form = LoginForm()
    result = handle_login(form)
    if result:
        return result
    return render_template('auth/login.html', title='Sign In', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth_bp.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        bmi = upsert_bmi(
            user_id=user.id,
            age=form.age.data,
            gender=form.gender.data,
            height=form.height.data,
            weight=form.weight.data
        )
        db.session.commit()
        login_user(user)
        session['show_welcome'] = True
        flash('Registration successful!')
        return redirect(url_for('dashboard_bp.dashboard'))
    return render_template('auth/register.html', title='Register', form=form) 