from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

# Define WTForm for lifestyle selection
class LifestyleForm(FlaskForm):
    lifestyle = SelectField(
        'Lifestyle',
        choices=[
            ('simple', '🌿 Simple Life'),
            ('quality', '✨ Quality Life'),
            ('luxury', '💎 Luxury Life')
        ],
        validators=[DataRequired(message="Please select a valid lifestyle.")]
    )
    submit = SubmitField("Confirm")


class ChangeLifestyleForm(FlaskForm):
    submit = SubmitField("Change Lifestyle")