from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField(
        "Email/Username",
        validators=[DataRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    fullname = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=3, max=100)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    username = StringField(
        "username",
        validators=[DataRequired()]
    )

    room_number = StringField(
        "Room Number",
        validators=[DataRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match")
        ]
    )

    submit = SubmitField("Register")


class ForgotPasswordForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    submit = SubmitField("Send Reset Link")