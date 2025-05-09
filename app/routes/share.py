from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.user import User
from app.models.share import Share
from app.models.comment import Comment
from app.models.categories import Category
from app import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

bp = Blueprint("share", __name__, url_prefix="/share")

# Define upload folder
UPLOAD_FOLDER = os.path.join("app", "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@bp.route("/", methods=["GET", "POST"])
@login_required
def share():
    # Get all categories
    categories = Category.query.all()

    if request.method == "POST":
        # Get form data
        category = request.form.get("category")
        title = request.form.get("title")
        content = request.form.get("content")
        link = request.form.get("link")
        is_public = request.form.get("is_public") == "on"
        receiver_input = request.form.get("receiver")
        receiver = None

        # Private share -> find receiver user
        if not is_public and receiver_input:
            receiver = User.query.filter(
                (User.username == receiver_input) | (User.email == receiver_input)
            ).first()
            if not receiver:
                flash("Receiver user not found.", "danger")
                return redirect(url_for("share.share"))

        # Handle uploaded image
        image_file = request.files.get("image")
        image_filename = None
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            image_file.save(image_path)

        # Create share record
        new_share = Share(
            sender_id=current_user.id,
            receiver_id=receiver.id if receiver else None,
            category=category,
            title=title,
            content=content,
            link=link,
            image=image_filename,
            is_public=is_public,
            timestamp=datetime.utcnow()
        )
        db.session.add(new_share)
        db.session.commit()

        flash("Share successful.", "success")
        return redirect(url_for("share.share"))

    # Load shares
    public_shares = Share.query.filter_by(is_public=True).order_by(Share.timestamp.desc()).all()
    sent_shares = Share.query.filter_by(sender_id=current_user.id).order_by(Share.timestamp.desc()).all()
    received_shares = Share.query.filter_by(receiver_id=current_user.id).order_by(Share.timestamp.desc()).all()

    return render_template("share.html",
                           public_shares=public_shares,
                           sent_shares=sent_shares,
                           received_shares=received_shares,
                           categories=categories)


@bp.route("/view/<int:share_id>", methods=["GET", "POST"])
@login_required
def view_share(share_id):
    share = Share.query.get_or_404(share_id)

    # Check permission
    if not share.is_public and current_user.id not in [share.sender_id, share.receiver_id]:
        flash("You do not have permission to view this share.", "danger")
        return redirect(url_for("share.share"))

    # Handle comment submission
    if request.method == "POST":
        comment_content = request.form.get("comment")
        parent_id = request.form.get("parent_id")  # Get parent comment ID from form

        if comment_content:
            new_comment = Comment(
                share_id=share.id,
                user_id=current_user.id,
                content=comment_content,
                parent_id=parent_id if parent_id else None  # Set parent_id if replying
            )
            db.session.add(new_comment)
            db.session.commit()
            flash("Comment added successfully!", "success")
            return redirect(url_for("share.view_share", share_id=share.id))

    # Get top-level comments only
    top_comments = Comment.query.filter_by(share_id=share.id, parent_id=None).order_by(Comment.timestamp).all()

    return render_template("view_share.html", share=share, comments=top_comments)



@bp.route("/my_shares")
@login_required
def my_shares():
    sent = Share.query.filter_by(sender_id=current_user.id).order_by(Share.timestamp.desc()).all()
    received = Share.query.filter_by(receiver_id=current_user.id).order_by(Share.timestamp.desc()).all()
    return render_template("my_shares.html", sent=sent, received=received)
