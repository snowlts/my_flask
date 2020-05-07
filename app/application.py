# # import os
# # basedir = os.path.abspath(os.path.dirname(__file__))
# # from datetime import datetime
# # from threading import Thread
# #
# # from flask import Flask,escape,url_for,request,render_template,flash,redirect,send_from_directory,abort,make_response,jsonify,session
# # from werkzeug.exceptions import RequestEntityTooLarge, HTTPException
# # from werkzeug.utils import secure_filename
# # from jinja2 import environment
# # from flask_bootstrap import Bootstrap
# # from flask_moment import Moment
# # from flask_mail import Mail,Message
# #
# # from flask_sqlalchemy import SQLAlchemy
#
# # print(os.path.dirname(__file__))
# # print(basedir)
# # from flask_migrate import Migrate
#
# # from flask_wtf import FlaskForm
# # from wtforms import StringField,SubmitField
# # from wtforms.validators import DataRequired
# #
# # class NameForm(FlaskForm):
# #     name = StringField('What is your name',validators=[DataRequired()])
# #     submit = SubmitField('Submit')
#
# # def filter_enumerate(alist):
# #     return enumerate(alist)
# #
# # environment.filters['enumerate']=filter_enumerate
#
# from app.models import User
#
# # UPLOAD_FOLDER = 'D:\Program Files\Python\my_flask\static'
# # ALLOWED_EXTENSIONS = {'txt','pdf','png','jpg','jpeg','gif'}
#
# # app = Flask(__name__)
# # app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
# # app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
# # app.config['SECRET_KEY'] = 'hard to guess string'
# #
# # app.config['MAIL_SERVER']='smtp.126.com'
# # app.config['MAIL_PORT']=25
# # app.config['MAIL_USE_TLS']=True
# #
# #
# # app.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME')
# # # print(app.config['MAIL_USERNAME'])
# # # print(os.environ.get('MAIL_USERNAME'))
# # app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWORD')
# # app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
# # app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <'+ os.environ.get('MAIL_USERNAME') +'>'
# # app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
# #
# # # with app.app_context():
# # #     mail.send(msg)
# #
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# # db = SQLAlchemy(app)
# # migrate = Migrate(app,db)
# # app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# app.secret_key=os.urandom(16)
# # bootstrap = Bootstrap(app)
# # moment = Moment(app)
# # mail = Mail(app)
#
#
#
# # class Role(db.Model):
# #     __tablename__='roles'
# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String(64), unique=True)
# #     users =db.relationship('User',backref='role', lazy='dynamic')
# #
# #     def __repr__(self):
# #         return '<Role %r>' % self.name
# #
# # class User(db.Model):
# #     __tablename__ = 'users'
# #     id = db.Column(db.Integer, primary_key = True)
# #     username = db.Column(db.String(64), unique=True, index=True)
# #     password = db.Column(db.String(64))
# #     phone = db.Column(db.String(64))
# #     address =db.Column(db.String(64))
# #     role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
#
#     # def __repr__(self):
#     #     return '<User %r>' % self.username
#
#
# # def send_async_email(app,msg):
# #     with app.app_context():
# #         mail.send(msg)
# #
# # def send_email(to, subject, template, **kwargs):
# #     msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
# #     sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
# #     msg.body = render_template(template + '.txt', **kwargs)
# #     msg.html = render_template(template + '.html', **kwargs)
# #     thr = Thread(target=send_async_email,args=[app,msg])
# #     thr.start()
# #     # mail.send(msg)
# #     return thr
# #
# # # msg=Message('testmail',sender="s@t.com",recipients=["s@t.com"])
# # # msg.body='Thisisaplaintextbody'
# # # msg.html='Thisisa<b>HTML</b>body'
# #
# # @app.shell_context_processor
# # def make_shel_context():
# #     return dict(db=db,User=User,Role=Role,mail=mail,Message=Message)
# #
# #
# # @app.route('/',methods=['GET','POST'])
# # def index():
# #     # username = session.get('username')
# #     users = session.get('username')
# #     if users:
# #         users = users.split(' ')
# #     return render_template('index.html',users=users,current_time =datetime.utcnow())
# #
# #
# # @app.route('/register',methods = ['GET','POST'])
# # def register():
# #     # print(app.config['SECRET_KEY'])
# #     # print(app.config['MAIL_PORT'])
# #     # print(app.config['FLASKY_ADMIN'])
# #     # print(app.config['MAIL_PASSWORD'])
# #     form = NameForm()
# #     if form.validate_on_submit():
# #         user = User.query.filter_by(username=form.name.data).first()
# #         if user is None:
# #             user = User(username=form.name.data)
# #             db.session.add(user)
# #             db.session.commit()
# #             session['known'] = False
# #             # print('hello')
# #             # print(app.config['FLASKY_ADMIN'])
# #             if app.config['FLASKY_ADMIN']:
# #                 # print('hello')
# #                 send_email(app.config['FLASKY_ADMIN'], 'New User',
# #                            'mail/new_user', user=user)
# #         else:
# #             session['known'] = True
# #         session['name'] = form.name.data
# #         # form.name.data = ''
# #         return redirect(url_for('register'))
# #     return render_template('register.html',form=form, name=session.get('name'),known=session.get('known', False))
# # # def register():
# # #     # name = None
# # #     form = NameForm()
# # #     if form.validate_on_submit():
# # #         oldname = session.get('name')
# # #         if oldname is not None and oldname!= form.name.data:
# # #             flash('Looks like you have changed your name!')
# # #             flash('1Looks like you have changed your name!')
# # #             flash('2Looks like you have changed your name!')
# # #         session['name'] = form.name.data
# # #         # form.name.data=''
# # #         return redirect(url_for('register'))
# # #     return render_template('register.html',form = form,name=session.get('name'))
# #
# # @app.route('/login',methods=['POST',"GET"])
# # def login():
# #     if request.method == 'POST':
# #         session['username'] = request.form['username']
# #         flash('You are successfully logged in','error')
# #         app.logger.debug('A value for debugging')
# #         app.logger.warning('A warning occurred (%d apples)', 42)
# #         app.logger.error('An error occurred')
# #         return redirect(url_for('index'))
# #     return '''
# #         <form method='POST' action='/login'>
# #             <p> <input type=text name = username> </p>
# #             <p> <input type=submit value=Login> </p>
# #         </form>
# #     '''
# # @app.route('/logout')
# # def logout():
# #     session.pop('username')
# #     return redirect(url_for('index'))
# #
# #
# # @app.route('/red')
# # def red():
# #     return redirect(url_for('error_abort'))
# #
# # @app.route('/fail')
# # def error_abort():
# #     abort(404)
# #
# #
# # def allowed_file(filename):
# #     return '.' in filename and \
# #            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# #
# # @app.route('/upload', methods=['GET', 'POST'])
# # def upload_file():
# #     if request.method == 'POST':
# #         # check if the post request has the file part
# #         if 'file' not in request.files:
# #             flash('No file part')
# #             return redirect(request.url)
# #         file = request.files['file']
# #         # if user does not select file, browser also
# #         # submit an empty part without filename
# #         if file.filename == '':
# #             flash('No selected file')
# #             return redirect(request.url)
# #         if file and allowed_file(file.filename):
# #             filename = secure_filename(file.filename)
# #             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# #             return redirect(url_for('uploaded_file',
# #                                     filename=filename))
# #     return '''
# #     <!doctype html>
# #     <title>Upload new File</title>
# #     <h1>Upload new File</h1>
# #     <form method=post enctype=multipart/form-data>
# #       <input type=file name=file>
# #       <input type=submit value=Upload>
# #     </form>
# #     '''
# #
# #
# # @app.route('/uploaded_file')
# # def uploaded_file():
# #     filename = request.args.get('filename')
# #     return render_template('uploaded_file.html',filename=filename)
# #
# # # @app.route('/uploaded_file/<filename>')
# # # def uploaded_file(filename):
# # #     return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
# #
# # @app.route('/hello/')
# # @app.route('/hello/<string:name>')
# # def hello(name=None):
# #     return render_template('index.html',name=name)
# #
# # # @app.route('/login',methods=['GET','POST'])
# # # def login():
# # #     print(request.method )
# # #     if request.method =='POST':
# # #         print('he')
# # #         username = request.form['username']
# # #         password = request.form['password']
# # #         return render_template('success.html',username=username,password=password)
# # #     else:
# # #         plant = request.args.get('plant')
# # #         return render_template('success.html')
# #
# #
# # @app.route('/user')
# # @app.route('/user/<username>')
# # def show_user_profile(username=None):
# #     # return datetime.now()
# #     # return ('Tom',404,{'XXX':123,'yyy':456})
# #     # return 'User %s' % username
# #     # return {'Tom':20}
# #     # users = [User('Tom','male',20),User('Jim','male',21),User('Bob','male',19),User('Kate','female',19)]
# #     # return jsonify([user.to_json() for user in users])
# #     # return '',302,{'location':'/'}
# #     # return 'Internal Error',404
# #     # abort(500)
# #     return render_template('user.html',username=username)
# #
# # @app.route('/post/<int:post_id>')
# # def show_post(post_id):
# #     # show the post with the given id, the id is an integer
# #     return 'Post %d' % post_id
# #
# # @app.route('/path/<path:subpath>')
# # def show_subpath(subpath):
# #     # show the subpath after /path/
# #     return 'Subpath %s' % escape(subpath)
#
# #
# #
# # @app.errorhandler(404)
# # def page_not_found(error):
# #     resp = make_response(render_template('404.html'),404)
# #     resp.headers['aaa']=111
# #     resp.headers['X-Something'] = 'A value'
# #     return resp
# #
# # @app.errorhandler(500)
# # def internal_error(error):
# #     return render_template('500.html'),500
#
# if __name__ == '__main__':
#     app.run(debug=True)
#     app_ctx = app.app_context()
#     app_ctx.push()
#     # with app.test_request_context():
#     #     print(url_for('index'))
#     #     print(url_for('login'))
#     #     print(url_for('login',next='/'))
#     #     print(url_for('show_user_profile',username='David Liu'))