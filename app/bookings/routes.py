from flask import request, redirect, url_for, flash, render_template
from sqlalchemy.orm import joinedload
from .models import Booking, Message
from app.extensions import db
from flask_login import current_user, login_required
from . import bookings_bp

@bookings_bp.route("/my_bookings")
@login_required
def my_bookings():
    # Retrieve all bookings for the logged-in user, with related expert and message details
    bookings = (
        Booking.query.filter_by(user_id=current_user.id)
        .options(joinedload(Booking.expert), joinedload(Booking.messages))
        .all()
    )

    return render_template("my_bookings.html", bookings=bookings)

@bookings_bp.route("/expert-dashboard")
@login_required
def expert_dashboard():
    expert_id = current_user.id  # Assuming the logged-in user is the expert
    db.session.expire_all()

    # Fetch the expert's bookings along with related messages and user details
    bookings = (
        Booking.query.filter_by(expert_id=expert_id)
        .options(joinedload(Booking.user), joinedload(Booking.messages))
        .all()
    )

    return render_template("expert-bookings.html", bookings=bookings)


@bookings_bp.route("/expert-reply_message/<int:booking_id>", methods=["POST"])
@login_required
def expert_reply_message(booking_id):
    """
    Route for users or experts to reply to a message within a specific booking.

    - Only the user or expert associated with the booking is authorized to send replies.
    - Retrieves the reply content from the form and creates a new Message record.
    - Saves the reply to the database and displays a success or error message.
    - Redirects the user back to the expert dashboard after handling the request.

    Parameters:
        booking_id (int): The ID of the booking associated with the message thread.
    """
    booking = Booking.query.get_or_404(booking_id)

    # Ensure only the booking's user or expert can reply
    if current_user.id not in [booking.user_id, booking.expert_id]:
        flash("You are not authorized to reply to this message.", "danger")
        return redirect(url_for("bookings.expert_dashboard"))

    reply_content = request.form.get("reply_content")

    if reply_content:
        # Log the current user's message
        new_message = Message(
            content=reply_content, booking_id=booking_id, sender_id=current_user.id
        )
        db.session.add(new_message)
        db.session.commit()

        flash("Your reply has been sent!", "success")
    else:
        flash("Please enter a reply to send.", "danger")

    return redirect(url_for("bookings.expert_dashboard"))


@bookings_bp.route("/reply_message/<int:booking_id>", methods=["POST"])
@login_required
def reply_message(booking_id):
    """
    Allows a user or expert to send a reply message in the context of a specific booking.

    - Ensures that only the user or expert associated with the booking can send a reply.
    - Accepts the reply content from the submitted form.
    - If valid, creates and saves a new Message associated with the booking and sender.
    - Redirects to the 'my_bookings' page after processing the reply.

    Parameters:
        booking_id (int): ID of the booking for which the reply is being sent.
    """
    booking = Booking.query.get_or_404(booking_id)

    # Ensure only the booking's user or expert can reply
    if current_user.id not in [booking.user_id, booking.expert_id]:
        flash("You are not authorized to reply to this message.", "danger")
        return redirect(url_for("bookings.my_bookings"))

    reply_content = request.form.get("reply_content")

    if reply_content:
        # Add a new message for the booking
        new_message = Message(
            content=reply_content, booking_id=booking_id, sender_id=current_user.id
        )
        db.session.add(new_message)
        db.session.commit()

        flash("Your reply has been sent!", "success")
    else:
        flash("Please enter a reply to send.", "danger")

    return redirect(url_for("bookings.my_bookings"))

@bookings_bp.route("/send_message/<int:booking_id>", methods=["POST"])
@login_required  # Ensure user is logged in before sending a message
def send_message(booking_id):
    user_id = current_user.id  # Get the logged-in user's ID
    message_content = request.form.get("message_content")

    if message_content:
        # Create a new message with the correct field names
        message = Message(
            sender_id=user_id, booking_id=booking_id, content=message_content
        )
        db.session.add(message)
        db.session.commit()

        flash("Your message has been sent!", "success")
        return redirect(
            url_for("bookings.expert_dashboard", booking_id=booking_id)
        )  # Redirect back to the booking details page
    else:
        flash("Please enter a message to send.", "danger")
        return redirect(url_for("bookings.expert_dashboard", booking_id=booking_id))


@bookings_bp.route("/update_booking_status/<int:booking_id>/<status>", methods=["POST"])
@login_required
def update_booking_status(booking_id, status):
    expert_id = current_user.id
    booking = Booking.query.get_or_404(booking_id)

    if booking.expert_id != expert_id:
        flash("You are not authorized to modify this booking.", "danger")
        return redirect(url_for("bookings.expert_dashboard"))

    if status not in ["Accepted", "Denied"]:
        flash("Invalid status.", "danger")
        return redirect(url_for("bookings.expert_dashboard"))

    booking.status = status
    db.session.commit()

    flash(f"Booking has been {status.lower()}!", "success")

    # You can add email notifications here if you want to notify the user about the status change
    return redirect(url_for("bookings.expert_dashboard"))
