from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Regexp
import phonenumbers


from app.database.models import User
from app.database.database import session_scope


class SignUpForm(FlaskForm):
    """Constructor for the Register Page"""
    first_name = StringField('First Name',
                             validators=[DataRequired(),
                                         Length(
                                 1, 30, message="Please provide a valid name"),
                                 Regexp(
                                 "^[A-Za-z][A-Za-z0-9_.]*$", 0,
                                 "Names must have only letters, numbers, dots or underscores",
                             )
                             ])

    last_name = StringField('Last Name',
                            validators=[DataRequired(),
                                        Length(
                                1, 30, message="Please provide a valid name"),
                                Regexp(
                                "^[A-Za-z][A-Za-z0-9_.]*$", 0,
                                "Names must have only letters, numbers, dots or underscores",
                            )
                            ])

    email = StringField('Email', validators=[
                        DataRequired(), Email(), Length(1, 64)])

    phone_number = StringField('Phone Number', validators=[
        DataRequired(), Length(1, 64)])

    password1 = PasswordField('Password', validators=[
                              DataRequired(), Length(6, 72)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(6, 72),
                                                              EqualTo('password1', message="Passwords must match!")])
    submit = SubmitField('Register')

    def validate_email(self, email):
        query = None
        with session_scope() as s:
            query = s.query(User).filter_by(
                email=email.data.lower().strip()).first()

        if query:
            raise ValidationError('Email already exists.')

    def validate_phone(self, phone_number):
        try:
            p = phonenumbers.parse(phone_number.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')


class LoginForm(FlaskForm):
    """Constructor for the Login Page"""
    email = StringField('Email', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(2, 72)])
    remember_me = BooleanField('Remember Me')  # if remember then sessions?
    submit = SubmitField('Login')

    def validate_email(self, email):
        email = email.data.lower().strip()
        if "@" in email:
            query = None
            with session_scope() as s:
                query = s.query(User).filter_by(email=email).first()

            if not query:
                raise ValidationError('This email is not registered.')
        else:
            raise ValidationError('Please provide a valid email address.')


class ContactUs(FlaskForm):
    """Constructor for the Contact Us Page"""
    subject = StringField('Subject of Inquiry', validators=[
                          DataRequired(), Length(1, 64)])
    message = TextAreaField('Message')
    send_copy = BooleanField('Send me a copy of my message')
    submit = SubmitField('Send')
