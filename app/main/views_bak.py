from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from flask_login import login_required

from threading import Thread

from flask import Flask,escape,url_for,request,render_template,flash,redirect,send_from_directory,abort,make_response,jsonify,session
from werkzeug.exceptions import RequestEntityTooLarge, HTTPException
from werkzeug.utils import secure_filename
from jinja2 import environment



@main.route('/')
def index():
    return render_template('index.html')



# msg=Message('testmail',sender="s@1t.com",recipients=["s@1t.com"])
# msg.body='Thisisaplaintextbody'
# msg.html='Thisisa<b>HTML</b>body'

# @main.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         # ...
#         return redirect(url_for('.index'))
#     return render_template('index.html',
#                             form=form, name=session.get('name'),
#                             known=session.get('known', False),
#                             current_time=datetime.utcnow())



# @main.route('/',methods=['GET','POST'])
# def index():
#     # username = session.get('username')
#     users = session.get('username')
#     if users:
#         users = users.split(' ')
#     return render_template('index.html',users=users,current_time =datetime.utcnow())


@main.route('/register',methods = ['GET','POST'])
def register():
    # print(app.config['SECRET_KEY'])
    # print(app.config['MAIL_PORT'])
    # print(app.config['FLASKY_ADMIN'])
    # print(app.config['MAIL_PASSWORD'])
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            # print('hello')
            # print(app.config['FLASKY_ADMIN'])
            if app.config['FLASKY_ADMIN']:
                # print('hello')
                send_email(app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        # form.name.data = ''
        return redirect(url_for('register'))
    return render_template('register.html',form=form, name=session.get('name'),known=session.get('known', False))
# def register():
#     # name = None
#     form = NameForm()
#     if form.validate_on_submit():
#         oldname = session.get('name')
#         if oldname is not None and oldname!= form.name.data:
#             flash('Looks like you have changed your name!')
#             flash('1Looks like you have changed your name!')
#             flash('2Looks like you have changed your name!')
#         session['name'] = form.name.data
#         # form.name.data=''
#         return redirect(url_for('register'))
#     return render_template('register.html',form = form,name=session.get('name'))

@main.route('/login',methods=['POST',"GET"])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        flash('You are successfully logged in','error')
        app.logger.debug('A value for debugging')
        app.logger.warning('A warning occurred (%d apples)', 42)
        app.logger.error('An error occurred')
        return redirect(url_for('index'))
    return '''
        <form method='POST' action='/login'>
            <p> <input type=text name = username> </p>
            <p> <input type=submit value=Login> </p>
        </form>    
    '''
@main.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))

@main.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'

@main.route('/red')
def red():
    return redirect(url_for('error_abort'))

@main.route('/fail')
def error_abort():
    abort(404)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@main.route('/uploaded_file')
@login_required
def uploaded_file():
    filename = request.args.get('filename')
    return render_template('uploaded_file.html',filename=filename)

# @main.route('/uploaded_file/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@main.route('/hello/')
@main.route('/hello/<string:name>')
def hello(name=None):
    return render_template('index.html',name=name)

# @main.route('/login',methods=['GET','POST'])
# def login():
#     print(request.method )
#     if request.method =='POST':
#         print('he')
#         username = request.form['username']
#         password = request.form['password']
#         return render_template('success.html',username=username,password=password)
#     else:
#         plant = request.args.get('plant')
#         return render_template('success.html')


@main.route('/user')
@main.route('/user/<username>')
def show_user_profile(username=None):
    # return datetime.now()
    # return ('Tom',404,{'XXX':123,'yyy':456})
    # return 'User %s' % username
    # return {'Tom':20}
    # users = [User('Tom','male',20),User('Jim','male',21),User('Bob','male',19),User('Kate','female',19)]
    # return jsonify([user.to_json() for user in users])
    # return '',302,{'location':'/'}
    # return 'Internal Error',404
    # abort(500)
    return render_template('user.html',username=username)

@main.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@main.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)
