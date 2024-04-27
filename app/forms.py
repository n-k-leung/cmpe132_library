from flask_wtf import FlaskForm
from flask import render_template
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    reg_role = StringField('Role', validators=[DataRequired(), validators.Length(max=32)], render_kw={"placeholder": "guest"})
    username = StringField('Username', validators=[DataRequired(), validators.Length(max=32)], render_kw={"placeholder": "guest_1"})
    email = StringField('Email', validators=[DataRequired(), validators.Length(max=32)], render_kw={"placeholder": "guest@sjsue.com"})
    password = PasswordField('Password', validators=[DataRequired(), validators.Length(max=32)])
    submit = SubmitField('Sign In')
    register = SubmitField('Register')

class HomeForm(FlaskForm):
    # maybe edit profile?
    edit = SubmitField('Edit')
class AdminForm(FlaskForm):
    #for editing roles
    edit = SubmitField('Edit')
class LogoutForm(FlaskForm):
    submit = SubmitField("I'm sure - Logout")

class DeleteAccountForm(FlaskForm):
    password = StringField(validators=[DataRequired(), validators.Length(max=32)])
    confirm = SubmitField("Confirm Account Deletion")

class AddBook(FlaskForm):
    title = StringField('Book name', validators=[DataRequired(), validators.Length(max=200)])
    author = StringField('Book author', validators=[DataRequired(), validators.Length(max=200)])
    submit = SubmitField('Add Book Item')

class RegisterForm(FlaskForm):
    reg_role  = StringField('Role', validators=[DataRequired(), validators.Length(max=32)], render_kw={"placeholder": "guest"})
    username = StringField('Username', validators=[DataRequired(), validators.Length(max=32)], render_kw={"placeholder": "guest_1"})
    email = StringField('Email', validators=[DataRequired(), validators.Length(max=32)], render_kw={"placeholder": "guest@sjsu.com"})
    #check if new password and confirm password are equal to each other
    password = PasswordField('New Password', [DataRequired(), EqualTo('confirm', message='Passwords must match'), validators.Length(max=32)])
    confirm  = PasswordField('Confirm Password', [DataRequired(), EqualTo('password', message='Passwords must match'), validators.Length(max=32)])
    submit = SubmitField('Submit')
    sign = SubmitField('Sign In')

