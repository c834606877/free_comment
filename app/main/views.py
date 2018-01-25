from flask import render_template, redirect, url_for, abort, request,\
current_app, make_response, send_from_directory, jsonify

from . import main
from .. import db

from ..models import Comment

from urllib import unquote

@main.route('/')
def index():
    return "H"

@main.route('/create', methods=['GET', 'POST'])
def createComment():
    url = request.values.get("url", '')
    comment = request.values.get("comment", '')
    name = request.values.get("name", '')
    parent_id = request.values.get("parent", '')

    if url == '' or comment == '' or parent_id == '':
        return 'url, comment, parent are needed', 500


    try:
        parent_id = int(parent_id)
    except ValueError:
        parent_id = -1

    if parent_id != -1:
        Comment.query.filter_by(url=url)\
            .filter_by(parent_id=parent_id).first_or_404();

    comm = Comment(url=url,body=comment, author_name=name,\
            parent_id=parent_id)
    db.session.add(comm)
    db.session.commit()
    return "{successful}"




@main.route('/get', methods=['GET', 'POST'])
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