import os

# print('balalala')
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

import sys
import click
from app import create_app, db
from app.models import User, Role,Permission,Post,Class,Student,Follow
from flask_migrate import Migrate,upgrade

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

# @main.shell_context_processor
# def make_shel_context():
#     return dict(db=db,User=User,Role=Role,mail=mail,Message=Message)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role,Post=Post,Permission=Permission,Class=Class,Student=Student,Follow=Follow)

@app.cli.command()
def deploy():
    """Run deployment tasks"""
    #migrate database to the latest revision
    upgrade()

    #create or update user roles
    Role.insert_roles()

    #ensure all users are following themselves
    User.add_self_follows()




@app.cli.command()
@click.option('--coverage/--no-coverage',default=False,
              help='Run tests under code coverage.')
@click.argument('test_names',nargs=-1)
def test(coverage,test_names):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE']='1'
        # print('sys.argv:',sys.argv)
        sys.exit(subprocess.call(sys.argv))
        # os.execvp(sys.executable, [sys.executable] + sys.argv)
    # COV = None
    # if coverage:
    #     import coverage
    #     COV = coverage.coverage(branch=True, include='app/*')
    #     COV.start()

    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir,'/tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

@app.cli.command()
@click.option('--length',default=25,help='Number of functions to include in the profiler report.')
@click.option('--profiler-dir',default=None,help='Directory where profiler data files are saved.')
def profile(length,profiler_dir):
    """Start the application under the code profiler."""
    from werkzeug.middleware.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app,restrictions=[length],profile_dir=profiler_dir)
    app.run(debug=False)


if __name__ == '__main__':
    app.run(debug=True)