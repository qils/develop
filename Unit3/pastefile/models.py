#!/usr/bin/evn python
# --*-- coding: utf-8 --*--

import os
import uuid
from datetime import datetime
from utils import get_file_path, get_file_md5
from ext import db


class PasteFile(db.Model):
    __tablename__ = 'pastefile'

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

    @property
    def path(self):
        return get_file_path(self.filehash)

    @classmethod
    def get_by_md5(cls, filemd5):
        pasted_file = cls.query.filter_by(filemd5=filemd5).first()
        return pasted_file

    @classmethod
    def create_by_upload_file(cls, upload_file):
        rst = cls(upload_file.filename, upload_file.mimetype, 0)
        upload_file.save(rst.path)      # 按uuid格式将文件保存在/tmp/permdir目录下

        with open(rst.path, 'rb') as f:
            filemd5 = get_file_md5(f)
            pasted_file = cls.get_by_md5(filemd5)

            if pasted_file:
                os.remove(rst.path)
                return pasted_file

            file_stat = os.stat(rst.path)
            rst.file_size = file_stat.st_size
            rst.filemd5 = filemd5

            db.session.add(rst)
            db.session.commit()
            return rst


