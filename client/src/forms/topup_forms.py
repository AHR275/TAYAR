from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class TopupForm(FlaskForm):

    room = StringField(
        "Room Number",
        validators=[DataRequired()]
    )

    amount = IntegerField(
        "Amount",
        validators=[
            DataRequired(),
            NumberRange(min=10, max=100)
        ]
    )

    submit = SubmitField("Continue To Payment")