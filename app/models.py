from datetime import datetime

import bleach
from markdown import markdown
from . import db

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, index=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    author_name = db.Column(db.String(64))
    author_email = db.Column(db.String(64))
    author_site = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean, default=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    #childcomment = db.relationship('Comment', backref='parent',
    #                               lazy='dynamic')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_comment = {
            'id': self.id,
            'url': self.url,
            'comment': self.body,
            'comment_html': self.body_html,
            'timestamp': self.timestamp.isoformat(),
            'name': self.author_name,
            'author_email': self.author_email,
            'author_site': self.author_site,
            'parent': self.parent_id
        }
        return json_comment

    
    @staticmethod
    def from_json(json_comment):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Comment(body=body)

db.event.listen(Comment.body, 'set', Comment.on_changed_body)