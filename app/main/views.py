from flask import render_template, redirect, url_for, abort, request,\
current_app, make_response, send_from_directory, jsonify

from . import main
from .. import db

from ..models import Comment

from urllib import unquote


@main.route('/')
def index():
    return redirect("/assets/index.html")

import json
from functools import wraps
from flask import redirect, request, current_app

def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f().data) + ')'
            return current_app.response_class(content, mimetype='application/json')
        else:
            return f(*args, **kwargs)
    return decorated_function


@main.route('/create', methods=['GET', 'POST'])
@support_jsonp
def createComment():
    url = request.values.get("url", '')
    comment = request.values.get("comment", '')
    name = request.values.get("name", '')
    parent_id = request.values.get("parent", '')

    if url == '' or comment == '' or parent_id == '':
        return 'url, comment, parent are needed', 500

    print url
    url = unquote(url)
    print "unquote: ", url



    try:
        parent_id = int(parent_id)
    except ValueError:
        parent_id = -1

    if parent_id != -1:
        Comment.query.filter_by(id=parent_id) \
                   .filter_by(url=url).first_or_404();

    comm = Comment(url=url,body=comment, author_name=name,\
            parent_id=parent_id)
    db.session.add(comm)
    db.session.commit()
    return jsonify({"success":"true"})




@main.route('/get', methods=['GET', 'POST'])
@support_jsonp
def getComment():
    url = request.values.get("url", '')
    if url == '':
        return {"return":"no url"}
    comments = Comment.query.filter_by(url=url).all()
    json = {
        "success":"true",
        "message": "",
        "comments":[comm.to_json() for comm in comments]
    }
    return jsonify(json)



@main.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('static/assets', path)
