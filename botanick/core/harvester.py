import threading
import subprocess
import os
import glob


class EngineThread (threading.Thread):
    """Thread used to call EmailHarvester for a specific engine (google, github, bing, etc...)."""

    def __init__(self, domain, engine):
        threading.Thread.__init__(self)
        self.domain = domain
        self.engine = engine

    def run(self):
        """Run function for this thread"""
        callEmailHarvester(self.domain, self.engine)


def callEmailHarvester(domain, engine):
    """
    Call EmailHarvester module.
    Arguments:
        domain -- the domain name (e.g. gmail.com)
        engine -- the engine name (e.g. google, github, bing, etc...)
    """
    command = " ".join(['emailharvester', 
               '-d', domain, 
               '-e', engine, 
               '-s', 'result_{0}.txt'.format(engine)])
    subprocess.call(command, shell=True)


def extractFileContent(filename):
    """
    Extract the EmailHarvester results into the result file.
    Arguments:
        filename -- the result file

    filename -- the result file
    """
    with open(filename) as f:
        return f.readlines()


def generateOutput(emails):
    return ", ".join(list(set(emails))).replace('\n', '') 


def generatedFiles():
    return glob.glob('./result_*.txt')


def generatedXMLFiles():
    return glob.glob('./result_*.xml')


def getResults():
    """Return all emails found by EmailHarvester."""
    emails = []
    for filename in generatedFiles():
        emails += extractFileContent(filename)
        os.remove(filename)
    for filename in generatedXMLFiles():
        os.remove(filename)
    return generateOutput(emails)

