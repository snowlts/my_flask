from . import api
from app import db
from ..models import Post,Permission,Comment
from flask import jsonify,request,g,url_for,current_app
from .decorators import permission_required
from .errors import forbidden

@api.route('/posts/')
def get_posts():
    page = request.args.get('page',1,type=int)
    pagination = Post.query.paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts=pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts',page=page-1)
    next =None
    if pagination.has_next:
        next = url_for('api.get_posts',page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev_url':prev,
        'next_url':next,
        'count':pagination.total
    })


@api.route('/posts/<int:id>')
def get_post(id):
    post=Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/posts/',methods=['POST'])
@permission_required(Permission.WRITE)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()),201,\
                   {'Location': url_for('api.get_post', id=post.id)}


@api.route('/posts/<int:id>',methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_post(id):
    post= Post.query.get_or_404(id)
    user = g.current_user
    if not user != post.author and \
        not user.can(Permission.ADMIN):
        return forbidden('Insufficient Permissions')
    post.body = request.json.get('body',post.body)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())


@api.route('/posts/<int:id>/comments/')
def get_post_comments(id):
    post = Post.query.get_or_404(id)
    comments = post.comments.all()
    return jsonify({'comments':[c.to_json() for c in comments]})

@api.route('/posts/<int:id>/comments/',methods=['POST'])
@permission_required(Permission.WRITE)
def new_post_comment(id):
    comment = Comment.from_json(request.json)
    comment.post_id=id
    comment.author_id = g.current_user
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()),201,\
           {'Location': url_for('api.get_post_comment',id=id)}

















