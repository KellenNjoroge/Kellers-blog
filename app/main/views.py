from flask import render_template, redirect, url_for, abort, request
from . import main
from ..models import User, Email, Blog, Comment
from flask_login import login_required, current_user
from .. import db, photos
from .forms import UpdateProfile, BlogForm, CommentForm, EmailForm
from ..user_emails import send_subscriptions, send_blogs
from datetime import datetime
from time import time, sleep
import markdown2


@main.route('/')
def index():
    """
    root page function that returns the index page and its data
    """
    form = EmailForm()

    if form.validate_on_submit():
        user_name = form.name.data
        user_email = form.email.data

        new_subscription = Email(name=user_name, email_data=user_email)
        new_subscription.save_email()

        send_subscriptions(new_subscription)
        return redirect(url_for('main.subscribed'))
    title = "Welcome | Keller's blog"

    return render_template("index.html", title=title, subscribe_form=form)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    update_form = UpdateProfile()

    if update_form.validate_on_submit():
        user.bio = update_form.bio.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username, id_user=user.id))
    title = 'Update Bio'
    return render_template('profile/update.html', form=update_form, title=title)


@main.route('/user/<uname>/update/userpic', methods=['POST'])
@login_required
def update_userpic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname, id_user=current_user.id))


@main.route('/blog/<int:id>', methods=['GET', 'POST'])
def blog(id):
    get_blog = Blog.query.get(id)
    get_blog_comments = Comment.get_blog_comments(id)

    if get_blog is None:
        abort(404)

    blog_format = markdown2.markdown(get_blog.blog_content, extras=["code-friendly", "fenced-code-blocks"])

    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        user_name = comment_form.name.data
        user_email = comment_form.email.data
        user_comment = comment_form.comment_data.data

        new_comment = Comment(name=user_name, email=user_email, comment_content=user_comment,
                              date_comment=datetime.now(), blog_id=id)
        new_comment.save_comment()

        return redirect(url_for('main.blog', id=id))

    get_comments = Comment.get_blog_comments(id)

    return render_template('blog.html', blog_format=blog_format, get_blog=get_blog, title="Blog",
                           comment_form=comment_form, get_comments=get_comments, comments_count=len(get_blog_comments))





@main.route('/blog/<int:id>/update/pic', methods=['POST'])
@login_required
def update_pic(id):
    blog = Blog.get_single_blog(id)
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        blog.blog_pic = path
        # user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('main.blog', id=id))
