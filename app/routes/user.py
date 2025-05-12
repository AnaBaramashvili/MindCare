from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.dal import get_bmi_by_user_id, update_user_profile
from app.extensions import db, csrf

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/profile', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def profile():
    user = current_user
    bmi = get_bmi_by_user_id(user.id)
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        age = int(request.form.get('age'))
        gender = request.form.get('gender')
        height = float(request.form.get('height'))
        weight = float(request.form.get('weight'))
        update_user_profile(user, username, email, bmi, age, gender, height, weight)
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('user_bp.profile'))
    return render_template('user/profile.html', user=user, bmi=bmi) 