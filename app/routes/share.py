from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify , abort
from flask_login import login_required, current_user
from app.models.user import User
from app.models.share import Share
from app.models.comment import Comment
from app.models.categories import Category
from app.forms.shareform import ShareForm
from app.forms.CommentForm import CommentForm 
from app.forms.deleteform import DeleteForm
from app import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

bp = Blueprint("share", __name__, url_prefix="/share")

UPLOAD_FOLDER = os.path.join("app", "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ========== Share Center Main ==========
@bp.route("/", methods=["GET", "POST"])
@login_required
def share():
    form = ShareForm()
    categories = Category.query.all()
    form.category.choices = [(c.category, c.category) for c in categories]

    if request.method == "POST" and form.validate_on_submit():
        receiver_input = form.receiver.data
        receiver = None

        if form.is_public.data == "off" and receiver_input:
            receiver = User.query.filter(
                (User.username.ilike(receiver_input)) | (User.email.ilike(receiver_input))
            ).first()
            if not receiver:
                flash("User not found.", "danger")
                return redirect(url_for("share.share"))

        image_file = form.image.data
        image_filename = None
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(UPLOAD_FOLDER, image_filename))

        new_share = Share(
            sender_id=current_user.id,
            receiver_id=receiver.id if receiver else None,
            category=form.category.data,
            title=form.title.data,
            content=form.content.data,
            image=image_filename,
            is_public=form.is_public.data == "on",
            timestamp=datetime.utcnow()
        )
        db.session.add(new_share)
        db.session.commit()
        flash("Share successful.", "success")
        return redirect(url_for("share.share"))
    else:
        # Handle validation errors
        for error in form.image.errors:
            flash(error, "danger")
    # Check the share data
    public_shares = Share.query.filter_by(is_public=True).order_by(Share.timestamp.desc()).all()
    sent_shares = Share.query.filter_by(sender_id=current_user.id).order_by(Share.timestamp.desc()).all()
    received_shares = Share.query.filter_by(receiver_id=current_user.id).order_by(Share.timestamp.desc()).all()

    
    delete_forms = {}
    for s in sent_shares:
        delete_forms[s.id] = DeleteForm()

    return render_template("share.html",
                           form=form,
                           public_shares=public_shares,
                           sent_shares=sent_shares,
                           received_shares=received_shares,
                           categories=categories,
                           delete_forms=delete_forms)


# ========== View Single Share ==========
@bp.route("/view/<int:share_id>", methods=["GET", "POST"])
@login_required
def view_share(share_id):
    share = Share.query.get_or_404(share_id)
    form = CommentForm()

    
    comments = Comment.query.filter_by(share_id=share.id, parent_id=None).order_by(Comment.timestamp).all()
    delete_forms = {}  # dict: comment_id -> DeleteForm()

    for comment in comments:
        delete_forms[comment.id] = DeleteForm()
        for reply in comment.replies:
            delete_forms[reply.id] = DeleteForm()

    if request.method == "POST" and form.validate_on_submit():
        new_comment = Comment(
            share_id=share.id,
            user_id=current_user.id,
            content=form.content.data,
            parent_id=form.parent_id.data or None
        )
        db.session.add(new_comment)
        db.session.commit()
        flash("Comment added.", "success")
        return redirect(url_for("share.view_share", share_id=share.id))

    return render_template("view_share.html", share=share, comments=comments, form=form, delete_forms=delete_forms)

# ========== Edit Share ==========
@bp.route("/edit/<int:share_id>", methods=["GET", "POST"])
@login_required
def edit_share(share_id):
    share = Share.query.get_or_404(share_id)
    if share.sender_id != current_user.id:
        flash("You cannot edit someone else's post.", "danger")
        return redirect(url_for("share.share"))

    categories = Category.query.all()

    if request.method == "POST":
        share.title = request.form.get("title")
        share.category = request.form.get("category")
        share.content = request.form.get("content")
        share.link = request.form.get("link")
        share.is_public = request.form.get("is_public") == "on"

        image_file = request.files.get("image")
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(UPLOAD_FOLDER, image_filename))
            share.image = image_filename

        db.session.commit()
        flash("Share updated successfully!", "success")
        return redirect(url_for("share.view_share", share_id=share.id))

    return render_template("edit_share.html", share=share, categories=categories)


# ========== Delete Share ==========
@bp.route("/delete/<int:share_id>", methods=["POST"])
@login_required
def delete_share(share_id):
    form = DeleteForm()  

    if not form.validate_on_submit():
        flash("Invalid CSRF token. Deletion failed.", "danger")
        return redirect(url_for("share.share"))

    share = Share.query.get_or_404(share_id)
    if share.sender_id != current_user.id:
        flash("You cannot delete someone else's post.", "danger")
        return redirect(url_for("share.share"))

    db.session.delete(share)
    db.session.commit()
    flash("Share deleted.", "success")
    return redirect(url_for("share.share"))

# ========== Delete Comment ==========
@bp.route("/comment/delete/<int:comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    # User can only delete their own comment
    if comment.user_id != current_user.id:
        flash("You do not have permission to delete this comment.", "danger")
        return redirect(url_for("share.view_share", share_id=comment.share_id))

    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted.", "success")
    return redirect(url_for("share.view_share", share_id=comment.share_id))

# ========== Edit Comment ==========
@bp.route("/comment/edit/<int:comment_id>", methods=["POST"])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if comment.user_id != current_user.id:
        return jsonify({"success": False, "message": "Permission denied"}), 403

    data = request.get_json()
    content = data.get("content", "").strip()

    if not content:
        return jsonify({"success": False, "message": "Content is empty"}), 400

    comment.content = content
    db.session.commit()
    return jsonify({"success": True})

# ========== Username Suggestion ==========
@bp.route("/suggest_users")
@login_required
def suggest_users():
    keyword = request.args.get("q", "")
    users = User.query.filter(User.username.ilike(f"%{keyword}%")).limit(5).all()
    return jsonify([u.username for u in users])
