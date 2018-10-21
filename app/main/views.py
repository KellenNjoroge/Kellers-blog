from flask import render_template, redirect, url_for, abort, request
from . import main
from ..models import User, Email
from flask_login import login_required, current_user
from .. import db, photos
from .forms import UpdateProfile, BlogForm, CommentForm, EmailForm
from ..user_emails import send_subscriptions, send_blogs


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
