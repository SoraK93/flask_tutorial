from flask_wtf import FlaskForm
from flaskblog import db
from flaskblog.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
	submit = SubmitField("Sign Up")

	def validate_username(self, username):
		user = db.session.execute(db.select(User).filter_by(username=username.data)).scalar_one_or_none()
		if user:
			raise ValidationError("That username is taken. Please choose a different one.")

	def validate_email(self, email):
		user = db.session.execute(db.select(User).filter_by(email=email.data)).scalar_one_or_none()
		if user:
			raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	remember = BooleanField("Remember Me")
	submit = SubmitField("Log In")
