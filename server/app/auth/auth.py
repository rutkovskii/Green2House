from app.database.database import session_scope
from app.database.models import User

from app.auth.forms import SignUpForm, LoginForm
from app.admin.config import ServerConfig

from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
    LoginManager,
)
import jwt
from datetime import datetime, timedelta
import secrets


login_manager = LoginManager()
auth_bp = Blueprint("auth_bp", __name__)


def __generate_rand_int():
    """Create a random int for the timedelta"""
    sr = secrets.SystemRandom()
    return sr.randrange(10001, 99999)


def generate_token(secret, payload):
    return jwt.encode(payload, secret, algorithm="HS256")


@auth_bp.route("/sign-up", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = SignUpForm()
    if form.validate_on_submit():
        name = " ".join([form.first_name.data.strip(), form.last_name.data.strip()])
        is_admin = False
        if name in ServerConfig.ADMINS:
            is_admin = True

        now = datetime.utcnow() + timedelta(seconds=__generate_rand_int())
        payload = {
            "val": now.strftime("%Y-%m-%d %H:%M:%S"),
        }

        user = User(
            phone_number=form.phone_number.data.strip(),
            name=" ".join([form.first_name.data.strip(), form.last_name.data.strip()]),
            email=form.email.data.lower().strip(),
            is_admin=is_admin,
            auth_token=generate_token(ServerConfig.SECRET_KEY, payload),
        )
        user.set_password(form.password1.data)

        with session_scope() as s:
            s.add(user)

        return redirect(url_for("auth_bp.signin"))

    return render_template("signup.html", form=form)


@auth_bp.route("/sign-in", methods=["GET", "POST"])
def signin():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for("home_bp.home"))

    if form.validate_on_submit():
        user = None
        if "@" in form.email.data:
            with session_scope() as s:
                user = (
                    s.query(User)
                    .filter_by(email=form.email.data.lower().strip())
                    .first()
                )

                s.expunge(user)

                if user is not None:
                    email = user.get_email()
                    name = user.get_name()
                    user_id = user.get_id()

                    session["email"] = email
                    session["name"] = name
                    session["user_id"] = user_id

        remember = True if request.form.get("remember_me") else False
        print("Remember Me: ", remember)
        print("User: ", user)
        if user and not user.check_password(form.password.data.strip()):
            flash("Invalid password.")
            return redirect(url_for("auth_bp.signin"))

        if login_user(user, remember=remember):
            return redirect(url_for("home_bp.home"))

        else:
            print("did not log in")

    return render_template("signin.html", form=form)


@login_manager.user_loader
def load_user(user_id):
    with session_scope() as s:
        user = s.query(User).filter_by(id=user_id).first()
        if user is not None:
            s.expunge(user)
    return user


@auth_bp.route("/sign-out")
@login_required
def signout():
    logout_user()
    return redirect(url_for("index_bp.index"))
