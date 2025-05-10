from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms.profileform import ProfileForm
from app import db  # Import the database instance

bp = Blueprint('profile', __name__, template_folder='templates')

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    success_message = None

    if form.validate_on_submit():
        # Update user details
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.gender = form.gender.data

        if form.password.data:
            current_user.set_password(form.password.data)  # Use the set_password method

        # Save changes to the database
        db.session.commit()

        # Flash success message
        flash('Profile updated successfully!', 'success')
        success_message = 'Profile updated successfully!'

    return render_template('profile.html', form=form, success_message=success_message)