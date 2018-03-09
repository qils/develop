#!/usr/bin/evn python
# --*-- coding: utf-8 --*--

import uuid
from datetime import datetime

from ext import db


class PasteFile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(128), nullable=False)
    filehash = db.Column(db.String(128), nullable=False, unique=True)
    filemd5 = db.Column(db.String(128), nullable=False, unique=True)
    file_size = db.Column(db.Integer, nullable=False)
    uploadtime = db.Column(db.DateTime, nullable=False)
    mimetype = db.Column(db.String(128), nullable=False)

    def __init__(self, filename='', mimetype='application/octet-stream', size=0, filehash=None, filemd5=None):
        self.uploadtime = datetime.now()
        self.filemd5 = filemd5
        self.mimetype = mimetype
        self.file_size = size
        self.filename = filename if filename else self.filehash
        self.filehash = filehash if filehash else self._hash_filename(filename)

    @staticmethod
    def _hash_filename(filename):
        _, _, suffix = filename.rpartition('.')
        return '{}.{}'.format(uuid.uuid4().hex, suffix)
