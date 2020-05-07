from datetime import datetime
from flask import render_template, session, redirect, url_for,current_app
from . import main
from .forms import NameForm,EditProfileForm,EditProfileAdminForm,PostForm,CommentForm
from .. import db
from ..models import User,Role,Post,Permission,Comment
from flask_login import login_required,current_user
from ..decorators import admin_required,permission_required

from threading import Thread

from flask import Flask,escape,url_for,request,render_template,flash,redirect,send_from_directory,abort,make_response,jsonify,session
from werkzeug.exceptions import RequestEntityTooLarge, HTTPException
from werkzeug.utils import secure_filename
from jinja2 import environment
from flask_sqlalchemy import get_debug_queries

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query:%s\nParameters:%s\nDuration:%fs\nContext:%s\n' %
                ( query.statement, query.parameters, query.duration, query.context))
    return response


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'

@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','',max_age=30*24*60*60)
    return resp

@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','1',max_age=30*24*60*60)
    return resp


@main.route('/',methods=['GET','POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post=Post(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page',1,type=int)
    show_followed=False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed',''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).\
        paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    posts = pagination.items
    return render_template('index.html',form=form,posts=posts,pagination=pagination,show_followed=show_followed)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    # posts = user.posts.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()). \
        paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    print(pagination)
    return render_template('user.html',user=user,posts=posts,pagination=pagination)

@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('main.user',username = current_user.username))
    form.name.data=current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form = form)


@main.route('/edit-profile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm()
    if form.validate_on_submit():
        user.email = form.email.data
        user.username=form.username.data
        user.confirmed=form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name=form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role.id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html',form=form)


@main.route('/post/<int:id>',methods=['GET','POST'])
def post(id,**kwargs):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,author_id=current_user.id,post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.post',id=id,page=-1))
    page = request.args.get('page',1,type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
               current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    query = Comment.query.filter_by(post_id=id)
    pagination = query.order_by(Comment.timestamp.desc()). \
        paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    # form.body.data = comment.body
    return render_template('post.html', posts=[post],form=form,comments=comments,pagination=pagination)


@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
        not current_user.is_administrator():
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post',id=post.id))
    form.body.data=post.body
    return render_template('edit_post.html',form = form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user= User.query.filter_by(username=username).first()
    if user is None:
        flash('invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash("Follow user {} success.".format(user.username))
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not follower of this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash("Unfollow user {} success.".format(user.username))
    return redirect(url_for('.user',username=username))

@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page',1,type=int)
    pagination = user.follower.paginate(
        page,per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user':f.follower,'timestamp':f.timestamp} for f in pagination.items]
    return render_template('follows.html',user=user,title="Followers of",
                           endpoint='.followers',pagination=pagination,
                           follows=follows)

@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page',1,type=int)
    pagination = user.followed.paginate(
        page,per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user':f.followed,'timestamp':f.timestamp} for f in pagination.items]
    return render_template('follows.html',user=user,title="Followed by",
                           endpoint='.followed_by',pagination=pagination,
                           follows=follows)


# @main.route('/edit_comment/<int:id>',methods=['GET','POST'])
# def edit_comment():
#     comment = Comment.query.get_or_404(id)
#     form=CommentForm()
#     if form.validate_on_submit():
#         comment.body=form.body.data
#         db.session.add(comment)
#         db.session.commit()
#         return redirect(url_for('.post',id=id,page=-1))
#     form.body.data=comment.body
#     return render_template()

@main.route('/delete_comment/<int:id>')
def delete_comment(id):
    comment=Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('.post',))


@main.route('/disable/<int:id>')
def disable():
    pass


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
    pagination=pagination, page=page)

@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))