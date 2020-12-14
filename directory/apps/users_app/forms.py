from flask_wtf import FlaskForm
from wtforms import PasswordField , StringField , SubmitField , BooleanField
from wtforms.validators import DataRequired , Length , EqualTo , Email , ValidationError
from wtforms.fields.html5 import EmailField
from .models import User
from flask_login import current_user 
from flask_wtf.file import FileField , FileAllowed
 
class RegisterationForm(FlaskForm):
    username = StringField('Username' , validators=[DataRequired(message='username must fill') , Length(min=2 , max=20)]) 
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password' , validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password' , validators=[DataRequired() , EqualTo('password')])
    submit = SubmitField('Sign Up')

    #Custom Validation For unique Username
    def validate_username(self , username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That Username is Taken')
    #Custom Validation For unique Email
    def validate_email(self , email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That Email is Taken')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password' , validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username' , validators=[DataRequired(message='username must fill') , Length(min=2 , max=20)]) 
    email = EmailField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture' , validators=[FileAllowed(['jpg' , 'png'])])
    submit = SubmitField('Update')

    #Custom Validation For unique Username
    def validate_username(self , username):
        if username.data !=  current_user.username: #check email field changed or not
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('That Username is Taken')
    #Custom Validation For unique Email
    def validate_email(self , email):
        if email.data !=  current_user.email: #check email field changed or not
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('That Email is Taken')

class RequestResetForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Email Reset Password')
    def validate_email(self , email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('User withe this Email Not Found')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password' , validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password' , validators=[DataRequired() , EqualTo('password')])
    submit = SubmitField('Reset Password')
    
