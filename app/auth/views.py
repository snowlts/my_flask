from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email

from .forms import LoginForm,RegistrationForm,PasswdUpdateForm,ResetPasswordForm,ResetPasswordRequestForm,EmailUpdateForm


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth'\
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm your account', 'auth/mail/confirm', user=current_user, token=token)
    flash('A confirmation mail has been sent to you by mail.')
    return redirect(url_for('main.index'))


@auth.route('/register',methods=['GET','POST'])
def register():
    # print(request.form)
    form = RegistrationForm()
    if form.validate_on_submit():
        # user = form.populate_obj(User())
        user=User(email=form.email.data,
                  username=form.username.data,
                  password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email,'Confirm your account','auth/mail/confirm',user=user,token=token)
        flash('A confirmation mail has been sent to you by mail.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # print(current_user.is_authenticated)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid mail or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/update/password',methods=['GET','POST'])
@login_required
def update_password():
    form = PasswdUpdateForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Password updated!')
            return redirect(url_for('main.index'))
        else:
            flash('Old password invalid!')
    return render_template('auth/update_password.html',form=form)

@auth.route('/update/email/request',methods=['GET','POST'])
@login_required
def update_email_request():
    form = EmailUpdateForm()
    form.default=current_user
    if form.validate_on_submit():
        pass
    return render_template('auth/update_email.html',form=form)




@auth.route('/reset',methods=['GET','POST'])
def send_reset_password_mail():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        #如果数据库有这个用户，发邮件
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Confirm your email', 'auth/mail/reset_password', user=user, token=token)
            flash('A reset password email has been sent to you by mail.')
            return redirect(url_for('auth.login'))
        #数据库没有这个用户，报错
        else:
            flash('Email not registered.')
    return render_template('auth/reset_password.html',form=form)

@auth.route('/reset/<token>',methods=['GET','POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    user = User.reset_password(token)
    if user:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()
            send_email(user.email,'Password reset.','auth/mail/password_reset',user=user)
            flash('Password reset success.')
            return redirect(url_for('main.index'))
        return render_template('auth/reset_password.html',form=form)
    flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

