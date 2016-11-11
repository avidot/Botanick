# -*- coding: utf-8 -*-
from flask import Flask
from core.harvester import engines
from core.harvester import EngineThread
from core.harvester import getResults


app = Flask("Botanick")


@app.route('/domain=<domain>')
def search(domain):
    """
    Search emails for a specific domain name.
    Arguments:
        domain -- the domain name
    """
    threads = []

    # Setup search engines
    for engine in engines:
        current_thread = EngineThread(domain, engine)
        current_thread.start()
        threads.append(current_thread)

    # Wait for all threads to complete
    for t in threads:
        t.join()

    return getResults()


def webservice():
    app.run(debug=True, host='0.0.0.0')
