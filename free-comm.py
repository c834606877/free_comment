#!/usr/bin/env python

import app
import os
from app import create_app, db
from app.models import Comment

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Comment=Comment)


@app.cli.command()
def deploy():
	db.create_all()


def main():
	app.run()


if __name__ == '__main__':
	main()