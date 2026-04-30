from typing import Optional

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, TextAreaField, IntegerField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional
from flask_wtf.file import FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    # Role choices: must select Volunteer or Organizer
    role = SelectField('Role', choices=[
        ('', 'Select Your Role'),
        ('Volunteer', 'Volunteer'),
        ('Organizer', 'Organizer')
    ], validators=[DataRequired(message='You must select a role.')])
    accept_rules = BooleanField('I accept the site rules', validators=[DataRequired()])
    submit = SubmitField('Register')


class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password (optional)')
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[Optional()])
    gender = RadioField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[Optional()])
    avatar = FileField('Upload Avatar', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    cv = FileField('Your CV (PDF)', validators=[FileAllowed(['pdf'], 'PDF only!')])
    submit = SubmitField('Update Profile')


class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired(), Length(min=3, max=120)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=5)])
    date = DateField('Date', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Create Event')

class FeedbackForm(FlaskForm):
    rating = IntegerField('Rating (1–5)', validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(min=3, max=500)])
    submit = SubmitField('Submit Feedback')

class ResultForm(FlaskForm):
    result_summary = TextAreaField('Event Results / Summary', validators=[DataRequired(), Length(min=3, max=1000)])
    submit = SubmitField('Save Results')

class JoinForm(FlaskForm):
    submit = SubmitField('Join Event')

class AdminRoleForm(FlaskForm):
    role = SelectField('Change Role', choices=[
        ('Volunteer', 'Volunteer'),
        ('Organizer', 'Organizer')
    ], validators=[DataRequired()])
    submit = SubmitField('Update Role')



class DisableUserForm(FlaskForm):
    reason = StringField("Ban Reason", validators=[DataRequired()])
    until = DateTimeLocalField("Ban Until (Leave blank for permanent ban)", format='%Y-%m-%dT%H:%M', validators=[Optional()])
    submit = SubmitField("Confirm Ban")

