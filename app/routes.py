import smtplib

from flask import current_app as app
from flask import render_template, flash, request, redirect, url_for

my_email = "udemycourses174@gmail.com"
password = "rznn ssbj rtjj ztfe"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/hydroponic")
def hydroponic():
    return render_template("hydroponic.html")


@app.route("/help")
def help():
    return render_template("help.html", title="Help")


@app.route("/resources")
def resources():
    return render_template("resources.html", title="Resources")



@app.route("/help/contact", methods=["POST"])
def send_support():
    # Handle form data
    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")

    # Construct the email message
    full_message = f"""
    Subject: {subject}

    From: {name} <{email}>
    
    Message:
    {message}
    """

    try:
        # Sending the email
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,  # Sending to your inbox
                msg=full_message,
            )
        flash(
            "Your message has been sent successfully. Our team will get back to you shortly.",
            "success",
        )
    except Exception as e:
        flash(f"An error occurred while sending your message: {str(e)}", "danger")

    return redirect(url_for("help"))  # Redirect back to the help page



@app.route("/contact", methods=["POST"])
def send_contact_message():
    # Handle form data
    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get(
        "subject", "Contact Form Submission"
    )  # Default subject if none is provided
    message = request.form.get("message")

    # Construct the email message
    full_message = f"""
    Subject: {subject}

    From: {name} <{email}>

    Message:
    {message}
    """

    try:
        # Sending the email
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,  # Sending to your inbox
                msg=f"Subject:{subject}\n\n{full_message}",
            )
        flash(
            "Your message has been sent successfully. Our team will get back to you shortly.",
            "success",
        )
    except Exception as e:
        flash(f"An error occurred while sending your message: {str(e)}", "danger")

    # Redirect back to the home page's contact section
    return redirect(url_for("home") + "#contact")