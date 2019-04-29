from flask import render_template,request,redirect,url_for, abort
from flask_login import login_required, current_user
from . import main
from .forms import PostForm, UpdateProfile, CommentForm
from ..models import Post, Comment, User, Star
from .. import db, photos
import markdown2
from ..request import get_quote


@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to IJPost'
    quote = get_quote()
    posts = Post.query.order_by(Post.posted_p.desc()).all()
    return render_template('index.html', title = title, quote = quote, posts=posts)


@main.route('/posts', methods=['GET', 'POST'])
def pickup():
    posts = Post.query.order_by(Post.posted_p.desc()).all()
    return render_template('posts.html', posts=posts)

@main.route('/post/new', methods = ['GET','POST'])
@login_required
def new_post():

    form = PostForm()
    my_stars = Star.query.filter_by(post_id=Post.id)

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        user_p = current_user

        new_post = Post(user_p=current_user._get_current_object().id, title=title, description = description)

        new_post.save_post()
        posts = Post.query.order_by(Post.posted_p.desc()).all()
        return render_template('posts.html', posts=posts)
    return render_template('new_post.html', form=form)


@main.route('/comment/new/<int:post_id>', methods = ['GET','POST'])
@login_required
def new_comment(post_id):
    form = CommentForm()
    post = Post.query.get(post_id)

    if form.validate_on_submit():
        comment = form.comment.data
         
        # Updated comment instance
        new_comment = Comment(comment=comment,user_c=current_user._get_current_object().id, post_id=post_id)

        # save comment method
        new_comment.save_comment()
        return redirect(url_for('.new_comment',post_id = post_id ))

    all_comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('comment.html', form=form, comments=all_comments, post=post)

@main.route('/post/star/<int:post_id>/star', methods=['GET', 'POST'])
@login_required
def star(post_id):
    post = Post.query.get(post_id)
    user = current_user
    post_stars = Star.query.filter_by(post_id=post_id)
    posts = Post.query.order_by(Post.posted_p.desc()).all()

    if Star.query.filter(Star.user_id == user.id, Star.post_id == post_id).first():
        return render_template('posts.html', posts=posts)

    new_star = Star(post_id=post_id, user=current_user)
    new_star.save_stars()
    
    return render_template('posts.html', posts=posts)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files: 
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname = uname))
    
