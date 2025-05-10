from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

# Define WTForm for Goal Input
class GoalForm(FlaskForm):  # Inherit from FlaskForm
    target_amount = FloatField(
        "Target Amount",
        validators=[
            DataRequired(message="Target amount is required."),
            NumberRange(min=1, message="Target amount must be greater than 0."),
        ],
    )
    years = IntegerField(
        "Years",
        validators=[
            DataRequired(message="Number of years is required."),
            NumberRange(min=1, max=50, message="Years must be between 1 and 50."),
        ],
    )
    submit = SubmitField("Set Goal")