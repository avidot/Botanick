# -*- coding: utf-8 -*-
import os
from flask import Flask
from botanick.core.harvester import harvest
from botanick.core.converters import tostring
from botanick.const import BASE_PATH


app = Flask("Botanick")


@app.route('/domain=<domain>')
def search(domain):
    """
    Search emails for a specific domain name.
    Arguments:
        domain -- the domain name
    """
    return tostring(harvest(domain))


@app.route('/')
def index():
    with open(os.path.join(BASE_PATH, 'botanick', 'templates', 'index.py')) as template:
        return "".join(template.readlines())


def webservice(args):
    app.run(debug=True, host=args['host'])
