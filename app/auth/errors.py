from flask import render_template,make_response
from . import auth

@auth.errorhandler(403)
def forbidden(e):
    return render_template('auth/403.html'),403

@auth.app_errorhandler(404)
def page_not_found(e):
    resp = make_response(render_template('404.html'), 404)
    # resp.headers['aaa'] = 111
    # resp.headers['X-Something'] = 'A value'
    return resp

@auth.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500