from flask import request, redirect, url_for, flash, render_template
from .models import Expert
from app.bookings.models import Booking
from app.extensions import db
from flask_login import current_user, login_required
from datetime import datetime
from . import users_bp as app

@app.route("/expert", methods=["GET", "POST"])
def expert():
    """
    Route to view available experts and book a session.

    - GET: Displays a list of all available experts to the user.
    - POST: Handles the booking of a session by the currently logged-in user.
        - Retrieves the selected expert, date, and time from the form.
        - Combines date and time into a datetime object.
        - Creates a new booking record in the database.
        - Associates the booking with the logged-in user using Flask-Login's `current_user`.

    On successful booking, the user is shown a flash message and redirected to the expert page.
    """
    experts = Expert.query.all()
    if request.method == "POST":
        expert_id = request.form.get("expert_id")
        session_date = request.form.get("session_date")
        session_time = request.form.get("session_time")

        # Combine the session date and time into a datetime object
        session_datetime = datetime.strptime(
            f"{session_date} {session_time}", "%Y-%m-%d %H:%M"
        )

        # Get the currently logged-in user's ID using Flask-Login's current_user
        user_id = current_user.id  # This captures the logged-in user's ID

        # Create a new booking with the logged-in user's ID
        new_booking = Booking(
            user_id=user_id, expert_id=expert_id, session_datetime=session_datetime
        )
        db.session.add(new_booking)
        db.session.commit()

        flash("Your session has been successfully booked!", "success")
        return redirect(url_for("users.expert"))

    return render_template("expert.html", experts=experts)

@app.route("/expert-settings", methods=["GET", "POST"])
@login_required
def expert_account_settings():
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
            url_for("users.expert_account_settings")
        )  # Ensure the function name matches here

    return render_template(
        "expert-settings.html", user=current_user
    )  # Template rendering


@app.route("/expert-help")
def expert_help():
    return render_template("expert-help.html", title="Help")

@app.route("/expert-help/contact", methods=["POST"])
@login_required
def expert_send_support():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    flash(
        "Your message has been sent successfully. Our team will get back to you shortly.",
        "success",
    )
    return redirect(url_for("users.expert_help"))
