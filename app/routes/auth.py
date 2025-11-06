from flask import Flask, render_template, redirect, session, url_for, flash, request, Blueprint
from flask_login import login_user, logout_user
from app.models import User, db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")  # 👈 Added url_prefix for cleaner routes

# ----------------- SIGN UP -----------------
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(Email=email).first()

        if existing_user:
            flash("Email already exists!", "error")
            return redirect(url_for("auth.signup"))

        new_user = User(Username=username, Email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Signup Successful!", "success")
        return redirect(url_for("auth.signin"))

    return render_template("signup.html")


# ----------------- SIGN IN -----------------
@auth_bp.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(Email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Login Successful!", "success")
            return redirect(url_for("note.home"))  # 👈 Make sure this route exists in your task blueprint
        else:
            flash("Invalid Credentials!", "error")
            return redirect(url_for("auth.signin"))

    return render_template("signin.html")


# ----------------- LOG OUT -----------------
@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Logout Successfully!", "info")
    return redirect(url_for("auth.signin"))
