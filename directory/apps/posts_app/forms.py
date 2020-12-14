from flask_wtf import FlaskForm
from wtforms import StringField , TextAreaField ,SubmitField
from wtforms.validators import DataRequired , Length , EqualTo , Email , ValidationError
from wtforms.fields.html5 import EmailField
from flask_login import current_user 
from flask_wtf.file import FileField , FileAllowed


class PostForm(FlaskForm):
    title = StringField('title' , validators=[DataRequired()])
    content = TextAreaField('Content' , validators=[DataRequired()])
    submit = SubmitField('Post')
