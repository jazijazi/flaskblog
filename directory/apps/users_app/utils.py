from flask import url_for , render_template
from directory import app , mail
import secrets
import os
from PIL import Image

def send_reset_email(user):
    token = user.get_reset_token()
    text = f"<h1>To Reset Your Password</h1> <br> \
        <h2> <a href={ url_for('users.reset_token' , token=token , _external=True) } >click heare</a> </h2>"

    mail.send_message(sender='password@flaskblog.com' , recipients=[user.email], subject='password reset' , html=render_template('users/reset_email_page.html',token=token))
    #print( url_for('users.reset_token' , token=token , _external=True) )

def send_confirm_token(user):
    token = user.get_confirm_token()
    text = f"<h1>To Reset Confirm your Account</h1> <br> \
        <h2> <a href={ url_for('users.confirm_account' , token=token , _external=True) } >click heare</a> </h2>"
    mail.send_message(sender='password@flaskblog.com' , recipients=[user.email], subject='Confirm Account' , html=text)
    print (text)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path , 'static/profile_pics' , picture_fn)
    
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn