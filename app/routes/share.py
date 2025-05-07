# Routes for forum: post creation, comment, like

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.post import Post
from datetime import datetime

# Define blueprint for share routes
bp = Blueprint("share", __name__)

@bp.route("/share", methods=["GET", "POST"])
@login_required
def share():
    # Handle forum post creation and display
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        new_post = Post(
            user_id=current_user.id,
            title=title,
            content=content,
            created_at=datetime.utcnow()
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Post created successfully", "success")
        return redirect(url_for("share.share"))
    posts = Post.query.all()
    return render_template("share.html", posts=posts)