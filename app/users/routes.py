from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.extensions import db
from . import users_bp


@users_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        # Collect form data
        username = request.form.get("username", current_user.username)
        email = request.form.get("email", current_user.email)
        address = request.form.get("address", current_user.address)
        phone = request.form.get("phone", current_user.phone)

        # Update user data with new information
        current_user.username = username
        current_user.email = email
        current_user.address = address
        current_user.phone = phone
        db.session.commit()

        return redirect(url_for("main.dashboard"))

    return render_template("profile.html", user=current_user)


@users_bp.route("/expert-profile", methods=["GET", "POST"])
@login_required
def expert_profile():
    if request.method == "POST":
        # Get form data
        username = request.form.get("username", current_user.username)
        email = request.form.get("email", current_user.email)
        role = request.form.get("role", current_user.role)
        address = request.form.get("address", current_user.address)
        phone = request.form.get("phone", current_user.phone)

        # Update user data and mark profile as complete
        current_user.username = username
        current_user.email = email
        current_user.address = address
        current_user.phone = phone
        current_user.profile_complete = True
        db.session.commit()  # Save changes to the database

        flash("Profile updated successfully!", "success")
        return redirect(url_for("bookings.expert_dashboard"))  # Redirect after update

    return render_template("expert-profile.html", user=current_user)


@users_bp.route("/settings", methods=["GET", "POST"])
@login_required
def account_settings():
    if request.method == "POST":
        # Handle the change password functionality
        if "change_password" in request.form:
            current_password = request.form.get("current_password")
            new_password = request.form.get("new_password")
            confirm_password = request.form.get("confirm_password")

            # Verify current password
            if not current_user.check_password(current_password):
                flash("Incorrect current password.", "error")
            elif new_password != confirm_password:
                flash("New password and confirmation do not match.", "error")
            else:
                # Update password
                current_user.set_password(new_password)
                db.session.commit()
                flash("Password updated successfully.", "success")

        # Handle the delete account functionality
        elif "delete_profile" in request.form:
            db.session.delete(current_user)
            db.session.commit()
            flash("Your account has been deleted successfully.", "success")
            return redirect(
                url_for("auth.login")
            )  # Redirect to the login page after deletion

        return redirect(
            url_for("users.account_settings")
        )  # Ensure the function name matches here

    return render_template("settings.html", user=current_user)  # Template rendering

