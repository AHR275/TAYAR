from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional
)


class ProfileForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=50)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "New Password",
        validators=[
            Optional(),
            Length(min=6)
        ]
    )

    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            Optional(),
            EqualTo(
                "password",
                message="Passwords must match."
            )
        ]
    )

    submit = SubmitField(
        "Save Changes"
    )