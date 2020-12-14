from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from directory import app , db
from flask_login import current_user
from flask import redirect , url_for , request
#add models
from directory.apps.posts_app.models import Post
from directory.apps.users_app.models import User

admin = Admin(app, name='microblog', template_mode='bootstrap4')

class BlogModelView(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    page_size = 20

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 1

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('users.login', next=request.url))

class PostModelView(BlogModelView):
    column_exclude_list = ['content', ]
    column_searchable_list = ['title', 'content']
    column_filters = ['date_posted']
    column_editable_list = ['title',]
    edit_modal = True
    create_modal = False
    form_excluded_columns = [] #To remove fields from the create and edit form

    form_widget_args = {
        'content': {
            'rows': 8,
            'style': 'color: black'
        }
    }

    can_export = True

class UserModelView(BlogModelView):
    column_exclude_list = ['password', ]
    column_searchable_list = ['username', 'email']
    column_filters = ['username' , 'email'] 
    column_editable_list = ['username' , 'active']
    edit_modal = False
    create_modal = False


admin.add_view(UserModelView(User, db.session))
admin.add_view(PostModelView(Post, db.session))

