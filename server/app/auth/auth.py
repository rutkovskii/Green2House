from app.database import Session
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from app.auth.forms import SignUpForm, LoginForm
from app.admin.config import ServerConfig

from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import LoginManager

login_manager = LoginManager()
auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/sign-up', methods=['GET', 'POST'])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = SignUpForm()
    if form.validate_on_submit():

        name = " ".join([form.first_name.data.strip(), form.last_name.data.strip()])
        is_admin = False
        if name in ServerConfig.ADMINS:
            is_admin = True

        user = User(
            phone_number=form.phone_number.data.strip(),
            name=" ".join([form.first_name.data.strip(), form.last_name.data.strip()]),
            email=form.email.data.lower().strip(),
            is_admin=is_admin
        )
        user.set_password(form.password1.data)

        session['email'] = user.get_email()
        session['name'] = user.get_name()

        s = Session()
        s.add(user)
        s.commit()
        s.close()

        return redirect(url_for('auth_bp.signin'))

    return render_template('signup.html', form=form)


@auth_bp.route('/sign-in', methods=['GET', 'POST'])
def signin():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('home_bp.home'))

    if form.validate_on_submit():
        user = None
        if "@" in form.email.data:
            s = Session()
            user = s.query(User).filter_by(email=form.email.data.lower().strip()).first()
            s.close()

            session['email'] = user.get_email()
            session['name'] = user.get_name()

        remember = True if request.form.get('remember_me') else False
        print('Remember Me: ', remember)
        if user and not user.check_password(form.password.data.strip()):
            flash('Invalid password.')
            return redirect(url_for('login'))

        if login_user(user, remember=remember):
            return redirect(url_for('home_bp.home'))

        else:
            print('did not log in')

    return render_template('signin.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    s = Session()
    user = s.query(User).filter_by(id=user_id).first()
    s.close()
    return user


@auth_bp.route('/sign-out')
@login_required
def signout():
    logout_user()
    return redirect(url_for('index_bp.index'))
