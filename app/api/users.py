
from . import api
from ..models import User,Post
from flask import jsonify

@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

@api.route('/users/<int:id>/posts/')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    posts = user.posts.all()
    return jsonify({'posts':[p.to_json() for p in posts]})


@api.route('/users/<int:id>/timeline/')
def get_users_followed(id):
    user = User.query.get_or_404(id)
    followed = user.followed_posts.all()
    return jsonify({'posts':[f.to_json() for f in followed]})

