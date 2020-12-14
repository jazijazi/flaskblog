from flask import Flask , render_template , flash , redirect , request , url_for 
from . import users
from .forms import RegisterationForm , LoginForm , UpdateAccountForm , RequestResetForm , ResetPasswordForm
from directory import app , db , bcrypt , mail
from .models import User
from .utils import send_reset_email , save_picture , send_confirm_token
from flask_login import login_user , logout_user , current_user , login_required
from sqlalchemy.exc import IntegrityError
import os

@users.route('/register/' , methods=['GET' , 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        new_user = User(username=form.username.data , email=form.email.data , password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            send_confirm_token(new_user)
        except IntegrityError:
            db.session.rollback()
            flash("Email Or Username In Use try Diffrent Email/Username" , 'danger')

        flash(f'Your Account has been Created Please confirm Your Email' , 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html' , title='Register' ,form=form)

@users.route('/confirm/')
def confirm_account():
    token =  request.args.get('token')
    user = User.verify_confirm_token(token)

    if not user :
        flash(f'User Not Found' , 'warning')
        return redirect(url_for('users.login'))
    if user.active :
        flash(f'USER ALREADY ACTIVE' , 'warning')
        return redirect(url_for('users.login'))
    user.active=True
    db.session.commit()    
    flash(f'Account Activate Now You Can Login' , 'success')
    return redirect(url_for('users.login'))       

@users.route('/login/' , methods=['GET' , 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data) and user.active:
            login_user(user , remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash(f'Login Unsuccessful Check Email/Password' , 'danger')
    return render_template('users/login.html' , title='Login' ,form=form)

@users.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('home'))

@users.route('/account/', methods=['GET' , 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        
        if form.picture.data:
            #delete old photo if exist and replace new photo with it
            if current_user.image_file != 'default.jpg':
                old_path = os.path.join(app.root_path , 'static' , 'profile_pics' , current_user.image_file)
                if os.path.exists(old_path):
                    os.remove(old_path)
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been Updated' , 'info')
        return redirect(url_for('users.account'))
    
    elif request.method=='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static' , filename='profile_pics/'+current_user.image_file)
    return render_template('users/account.html' , title='Account' , image_file=image_file , form=form)

@users.route('/reset_password/' , methods=['GET' , 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email has been sent to reset your password' , 'info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html' , title='Reset Password' , form=form)

@users.route('/reset_password/<token>' , methods=['GET' , 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    user = User.verify_reset_token(token)

    if user is None :
        flash('That is an invalid or expired token' , 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your Password has benn Updated' , 'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_token.html' , title='Reset Password' , form=form)