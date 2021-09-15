from flask import Blueprint, render_template, request, flash, redirect, url_for, Markup
from SRP import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from SRP.models import srp_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = srp_user.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, please try again.", category="error")
        else:
            flash("This e-mail does not exist in the database.  Please register first.", category="error")
            return redirect(url_for('auth.register'))
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    # data = request.form
    # print(data)
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user = srp_user.query.filter_by(email=email).first()

        if user:
            flash("This e-mail has already been registered.  Please login.", category="error")
            return redirect(url_for("auth.login"))
        elif True and "@dea.aero" not in email:
            flash("Please use your company e-mail.", category="error")
        elif password1 != password2:
            flash("Please correctly confirm your chosen password.", category="error")
        else:
            new_user = srp_user(email=email, username=username,
                                password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    return render_template("register.html", user=current_user)
