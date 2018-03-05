#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import click
from flask import Flask


app = Flask(__name__, template_folder='../templates/', static_folder='../static/')


@app.cli.add_command(name='initdb')
def initdb():
    click.echo('This is a test')
