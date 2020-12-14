from flask import Flask , render_template
from directory.config import Development
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object(Development)

#EMAIL
mail = Mail(app)

#Databese
db = SQLAlchemy(app)
migrate = Migrate(app , db)

#Bcrypt
bcrypt = Bcrypt(app)

#Loginmanager
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message = 'Please login to access this page!'
login_manager.login_message_category = 'warning'

#Register Blueprints
from directory.apps.users_app import users
from directory.apps.posts_app import posts
from directory.apps.errors_app import errors

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(errors)

from directory.apps.admin_app import admin

