from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from wtforms import Form, StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from datetime import datetime
from app import db
from app.models.post import Post

# Define blueprint for share routes
bp = Blueprint("share", __name__)

# WTForm for Forum Post
class PostForm(Form):
    title = StringField(
        "Title",
        validators=[
            DataRequired(message="Title is required."),
            Length(max=100, message="Title must be less than 100 characters."),
        ],
    )
    content = TextAreaField(
        "Content",
        validators=[
            DataRequired(message="Content is required."),
            Length(max=1000, message="Content must be less than 1000 characters."),
        ],
    )

@bp.route("/share", methods=["GET", "POST"])
@login_required
def share():
    # Create an instance of the PostForm
    form = PostForm(request.form)

    # Handle form submission
    if request.method == "POST" and form.validate():
        title = form.title.data
        content = form.content.data
        new_post = Post(
            user_id=current_user.id,
            title=title,
            content=content,
            created_at=datetime.utcnow(),
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Post created successfully", "success")
        return redirect(url_for("share.share"))
    elif request.method == "POST" and not form.validate():
        # If the form is invalid, flash the errors
        flash("Please correct the errors in the form.", "danger")

    # Retrieve all posts to display them
    posts = Post.query.all()
    return render_template("share.html", form=form, posts=posts)