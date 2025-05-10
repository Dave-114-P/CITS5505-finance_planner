from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    content = TextAreaField("Comment", validators=[DataRequired()])
    parent_id = HiddenField()
    submit = SubmitField("Submit Comment")
