from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length

class CommentForm(FlaskForm):
    content = TextAreaField("Comment", validators=[
        DataRequired(message="Comment cannot be empty."),
        Length(max=500, message="Comment must be under 500 characters.")
        ])
    parent_id = HiddenField()
    submit = SubmitField("Submit Comment")
