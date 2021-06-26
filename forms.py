"""Forms for Flask-Feedback"""

from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)],)
    password = PasswordField("Password", validate_on_submit=[InputRequired(), Length(min=8, max=60)],)

class RegisterForm(FlaskForm):
    """New User Registration Form"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)],)
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55)],)
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=50)],)
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)],)
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)],)

class FeedbackForm(FlaskForm):
    """Form to Add Feedback"""

    title = StringField("Title", validators=[InputRequired(), Length(max=75)],)
    description = StringField("Description", validators=[InputRequired()],)

class DeleteForm(FlaskForm):
    """Delete Form"""
