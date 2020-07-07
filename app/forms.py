from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()]) # Don't need to waste time checking email
    # Use pip install email-validator
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Re-enter Password', validators=[DataRequired(),
                                                               EqualTo('password')])
    submit = SubmitField('Register')

    # WTFforms takes methods that have validate_<email> as extra validators
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please user a different username. It is already taken!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email. Someone with the same email already exists in our DB!')


class EditProfileForm(FlaskForm):
    username = StringField('New username:', validators=[DataRequired()]) # What if they don't want to change username?
    about_me = TextAreaField('About me:', validators=[Length(0,140)])
    submit = SubmitField('Submit')


    # To fix the bug with the username!
    def __init__(self, original_username, *args, **kwargs): # constructor
        super(EditProfileForm, self).__init__(*args, **kwargs) # using super for inheritance
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError("Please choose a different username. This one is already assigned.")

# Form that only does a submit action, but use this for the post request
# This will allow you to know if want to follow or unfollow
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')