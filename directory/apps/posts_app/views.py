from . import posts
from .models import Post
from directory.apps.users_app.models import User
from .forms import PostForm
from flask import Flask , render_template , flash , redirect , request , url_for , abort
from directory import app , db , bcrypt
from flask_login import current_user , login_required

@app.route('/home/')
@app.route('/')
def home():
    page = request.args.get('page' , 1 , type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page , 1)
    return render_template('home.html' , posts=posts)

@posts.route('/post/new/' , methods=['GET' , 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        
        new_post = Post(title=form.title.data , content=form.content.data , author=current_user)
        db.session.add(new_post)
        db.session.commit()
        
        flash('Your Post has been created' , 'success')
        return redirect(url_for('home'))
    return render_template('posts/create_post.html' , title='New Post' , legend="Create Post" , form=form)

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post.html' , title=post.title , post=post)

@posts.route('/post/<int:post_id>/update/' , methods=['GET' , 'POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user :
        abort(403)
    
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post has been updated' , 'success')
        return redirect(url_for('posts.post' , post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content 

    return render_template('posts/create_post.html' , title='Update Post' , legend="Update Post" , form=form)

@posts.route('/post/<int:post_id>/delete/' , methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user :
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted' , 'success')
    return redirect(url_for('home'))

@posts.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page' , 1 , type=int)
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page , 1)
    return render_template('/posts/user_posts.html' , posts=posts , user=user)