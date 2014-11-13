#!/usr/bin/env python

from flask.ext.script import Manager
from flask.ext.script.commands import ShowUrls, Clean

from app import app, db


manager = Manager(app)
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())


@manager.command
def db():
    """ Creates a database with all of the tables defined in
        your Alchemy models
    """

    db.create_all()

if __name__ == '__main__':
    manager.run()