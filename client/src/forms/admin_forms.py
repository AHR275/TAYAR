from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField , DecimalField , HiddenField
from wtforms.validators import DataRequired, Email



class CreateUserForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[DataRequired()]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Add User")

class UpdateUserForm(FlaskForm):

    user_id = HiddenField(
        validators=[DataRequired()]
    )

    username = StringField(
        validators=[DataRequired()]
    )

    email = StringField(
        validators=[DataRequired(), Email()]
    )

    submit = SubmitField("Save")

class DeleteUserForm(FlaskForm):

    user_id = HiddenField(
        validators=[DataRequired()]
    )

    submit = SubmitField("Delete")



class CreateRoomForm(FlaskForm):

    room_number = StringField(
        validators=[DataRequired()]
    )

    building = StringField(
        validators=[DataRequired()]
    )

    balance = DecimalField(
        validators=[DataRequired()]
    )

    submit = SubmitField("Add Room")


class UpdateRoomForm(FlaskForm):

    room_id = HiddenField(
        validators=[DataRequired()]
    )

    room_number = StringField(
        validators=[DataRequired()]
    )

    building = StringField(
        validators=[DataRequired()]
    )

    balance = DecimalField(
        validators=[DataRequired()]
    )

    submit = SubmitField("Save")


class DeleteRoomForm(FlaskForm):

    room_id = HiddenField(
        validators=[DataRequired()]
    )

    submit = SubmitField("Delete")