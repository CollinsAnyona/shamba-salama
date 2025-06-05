from app.extensions import db
from .models import User
from .utils import assign_avatar
from flask import render_template, request, redirect, url_for, flash, Blueprint, render_template

from flask_login import (
    login_user,
    LoginManager,
)
from . import auth_bp

login_manager = LoginManager()
login_manager.init_app(auth_bp)
login_manager.login_view = "auth.login"



@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Handle registration
        if request.form.get("form_type") == "register":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            role = request.form.get("role")
            gender = request.form.get("gender")  # Capture gender input

            # Check if user already exists
            if User.query.filter_by(username=username).first():
                flash("Username already taken")
                return redirect(url_for("auth.login") + "#register-form")
            if User.query.filter_by(email=email).first():
                flash("Email already in use")
                return redirect(url_for("auth.login") + "#register-form")

            # Assign an avatar based on gender
            avatar_name = assign_avatar(gender)

            # Register new user
            new_user = User(
                username=username,
                email=email,
                role=role,
                gender=gender,
                profile_image_url=avatar_name,
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.")
            return redirect(url_for("auth.login"))

        elif request.form.get("form_type") == "login":
            user = User.query.filter_by(email=request.form["email"]).first()
            if user and user.check_password(request.form["password"]):
                login_user(user)

                # Redirect based on the user's role and profile completion status
                if not user.profile_complete:
                    if user.role == "farmer":
                        return redirect(url_for("users.profile"))
                    elif user.role == "expert":
                        return redirect(url_for("users.expert_profile"))

                # Check role and redirect accordingly
                if user.role == "farmer":
                    return redirect(url_for("users.dashboard"))
                elif user.role == "expert":
                    return redirect(url_for("users.expert_dashboard"))

            flash("Invalid credentials", "error")
            return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    return render_template("login.html", title="Logout")