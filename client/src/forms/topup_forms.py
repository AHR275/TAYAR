from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class TopupForm(FlaskForm):

    building = SelectField(
        "Building",
        validators=[DataRequired()],
        choices=[]
    )

    room = SelectField(
        "Room",
        
        choices=[],
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