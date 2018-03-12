#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from ext import db
from models import PasteFile
from app import app
from flask_script import Manager, Shell, Server, prompt_bool


manage = Manager(app)


@manage.command
def drop_all():
    if prompt_bool(
        '''
        Are you sure drop all table?
        '''
    ):
        db.drop_all()


def make_shell_context():
    return {
        'db': db,
        'PasteFile': PasteFile,
        'app': app
    }


manage.add_command('shell', Shell(make_context=make_shell_context))
manage.add_command('runserver', Server(host='0.0.0.0', port=8888, use_reloader=True, use_debugger=True))


@manage.option('-h', '--filehash', dest='filehash')
def get_file_by_hash(filehash):
    pastefile = PasteFile.query.filter_by(filehash=filehash).first()
    if not pastefile:
        print 'Not exists'
    else:
        print 'filename: {}'.format(pastefile.filename)


if __name__ == '__main__':
    manage.run()
