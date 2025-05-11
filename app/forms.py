from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, NumberRange, InputRequired
from datetime import date


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
   

def validate_gender(form, field):
    if field.data == '':
        raise ValidationError('Please select your gender.')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Select Gender', choices=[('', 'Select Gender'),('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired(), validate_gender])
    height = FloatField('Height (cm)', validators=[DataRequired()])
    weight = FloatField('Weight (kg)', validators=[DataRequired()])
    submit = SubmitField('Register')



class HealthLogForm(FlaskForm):
    sleep_hours = FloatField('Sleep Hours', validators=[InputRequired(), NumberRange(min=0, max=24)])
    exercise_minutes = IntegerField('Exercise Minutes', validators=[InputRequired(), NumberRange(min=0)])
    date = DateField("Date", default=date.today, format='%Y-%m-%d')
    submit = SubmitField('Log Entry')