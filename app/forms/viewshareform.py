from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length

class CommentForm(FlaskForm):
    parent_id = HiddenField("Parent ID")
    comment = TextAreaField(
        "Comment",
        validators=[
            DataRequired(message="Comment cannot be empty."),
            Length(max=500, message="Comment must be under 500 characters."),
        ],
        render_kw={"placeholder": "Write something..."},
    )
    submit = SubmitField("Submit Comment")