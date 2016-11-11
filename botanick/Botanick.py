# -*- coding: utf-8 -*-

import sys
import threading
import subprocess
import os
from flask import Flask
import glob

app = Flask(__name__)
engines = ["google", "linkedin", "bing", "yahoo", "github"]


class myThread (threading.Thread):

    def __init__(self, domain, engine):
        threading.Thread.__init__(self)
        self.domain = domain
        self.engine = engine

    def run(self):
        callEmailHarvester(self.domain, self.engine)


def callEmailHarvester(domain, engine):
    commandToCall = 'emailharvester -d '
    commandToCall += domain
    commandToCall += ' -e '
    commandToCall += engine
    commandToCall += ' -s result_'
    commandToCall += engine
    commandToCall += '.txt'
    subprocess.call(commandToCall, shell=True)


def extractFileContent(filename):
    with open(filename) as f:
        return f.readlines()


def generateOutput(emails):
    return ", ".join(list(set(emails))).replace('\n', '') 


def generatedFiles():
    return glob.glob('./result_*.txt')


def getResults():
    emails = []
    for filename in generatedFiles():
        emails += extractFileContent(filename)
        os.remove(filename)
    return generateOutput(emails)


@app.route('/domain=<domain>')
def search(domain):
    threads = []

    # Setup search engines
    for engine in engines:
        current_thread = myThread(domain, engine)
        current_thread.start()
        threads.append(current_thread)

    # Wait for all threads to complete
    for t in threads:
        t.join()

    return getResults()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
