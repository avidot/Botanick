# -*- coding: utf-8 -*-
from flask import Flask
from botanick.core.harvester import harvest
from botanick.core.converters import tostring


app = Flask("Botanick")


@app.route('/domain=<domain>')
def search(domain):
    """
    Search emails for a specific domain name.
    Arguments:
        domain -- the domain name
    """
    return tostring(harvest(domain))


def webservice(args):
    app.run(debug=True, host=args['host'])
