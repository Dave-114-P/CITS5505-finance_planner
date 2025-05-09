from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SelectField, RadioField, SubmitField
from wtforms.validators import DataRequired, Optional, Length
from flask_wtf.file import FileAllowed

class ShareForm(FlaskForm):
    receiver = StringField(
        "Receiver (username or email)",
        validators=[Optional()],
        render_kw={"placeholder": "Leave blank for public share"},
    )
    category = SelectField(
        "Category", validators=[DataRequired(message="Category is required.")]
    )
    title = StringField(
        "Title",
        validators=[
            DataRequired(message="Title is required."),
            Length(max=100, message="Title must be 100 characters or less."),
        ],
        render_kw={"placeholder": "Enter your share title"},
    )
    content = TextAreaField(
        "Content",
        validators=[Optional()],
        render_kw={"placeholder": "Write your thoughts or details here..."},
    )
    image = FileField(
        "Upload Image",
        validators=[Optional(), FileAllowed(["jpg", "jpeg", "png"], "Images only!")],
    )
    is_public = RadioField(
        "Share Type",
        choices=[("off", "Private"), ("on", "Public")],
        default="off",
        validators=[DataRequired()],
    )
    submit = SubmitField("Share")