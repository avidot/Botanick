import threading
import subprocess
import os
import glob


engines = ["google", "linkedin", "bing", "yahoo", "github"]


class EngineThread (threading.Thread):
    """Thread used to call EmailHarvester for a specific engine (google, github, bing, etc...)."""

    def __init__(self, domain, engine):
        threading.Thread.__init__(self)
        self.domain = domain
        self.engine = engine

    def run(self):
        """Run function for this thread"""
        emailHarvester(self.domain, self.engine)


def emailHarvester(domain, engine):
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


def extract(filename):
    """
    Extract the EmailHarvester results into the result file.
    Arguments:
        filename -- the result file

    filename -- the result file
    """
    with open(filename) as f:
        return f.readlines()


def lsfiles():
    """
    List all generated files (txt and xml).
    """
    return glob.glob('./result_*.txt'), glob.glob('./result_*.xml')


def files(extension="txt"):
    """
    List all file with specified extension (txt and xml).
    Arguments:
        extension -- extension to search
    """
    txtfiles, xmlfiles = lsfiles()
    if extension=="txt":
        return txtfiles
    elif extension=="xml":
        return xmlfiles
    else:
        raise ValueError("Bad extension format (txt, xml)")


def clean(filename):
    """
    Remove specified file (txt and xml).
    Arguments:
        filename -- file to delete
    """
    os.remove(filename)
    os.remove(filename.replace("txt", 'xml'))


def results():
    """Return all emails found by EmailHarvester."""
    emails = []
    for filename in files():
        emails += extract(filename)
        clean(filename)
    return emails


def harvest(domain):
    """
    Search emails for a specific domain name.
    Arguments:
        domain -- the domain name
    """
    threads = []
    for engine in engines:
        current_thread = EngineThread(domain, engine)
        current_thread.start()
        threads.append(current_thread)
    for t in threads:
        t.join()
    return results()
