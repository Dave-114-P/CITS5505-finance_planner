from flask_wtf import FlaskForm
from wtforms import FloatField, DateField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, ValidationError
from datetime import date

# Custom validator to ensure the date is not in the future
def validate_date_not_in_future(form, field):
    if field.data > date.today():
        raise ValidationError("The date cannot be in the future.")

class IncomeForm(FlaskForm):
    amount = FloatField(
        "Amount ($)",
        validators=[
            DataRequired(message="Amount is required."),
            NumberRange(min=0.01, message="Amount must be greater than zero.")
        ],
        render_kw={"class": "form-control", "step": "0.01", "id": "amount", "style": "color: #8ec23b;"}
    )
    category = SelectField(
        "Category",
        choices=[
            ("", "Select a category"),
            ("Interest", "Interest"),
            ("Salary", "Salary"),
            ("Cashback", "Cash back")
        ],
        validators=[DataRequired(message="Please select a category.")],
        render_kw={"class": "form-select", "id": "category"}
    )
    date = DateField(
        "Date",
        validators=[
            DataRequired(message="Date is required."),
            validate_date_not_in_future
        ],
        render_kw={"class": "form-control", "id": "date"}
    )
    description = TextAreaField(
        "Description (Optional)",
        validators=[Optional()],
        render_kw={"class": "form-control", "rows": 3, "id": "description"}
    )
    submit = SubmitField(
        "UPLOAD",
        render_kw={"class": "btn btn-primary", "style": "background-color: #ddd0c2; border: #ddd0c2; width: 150px; text-align: center;"}
    )
