# -*- coding: utf-8 -*-

import _thread
import threading
import time
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
        
def callEmailHarvester(domain,engine):
    result = subprocess.call('emailharvester -d '+domain+' -e '+engine+' -s result_'+engine+'.txt', shell=True)
    
def extractFileContent(filename):
    emails_found=""
    with open(filename) as f:
        for line in f:
            if line not in emails_found:
                if emails_found == "":
                    emails_found=line
                else:
                    emails_found=emails_found+", "+line
    return emails_found
    
def getResults():
    list_of_files = glob.glob('./result_*.txt')
    emails_found=""
    for file_name in list_of_files:
        emails_found += extractFileContent(file_name)
        os.remove(file_name)
    return emails_found


def search2(domain):
    return "test"

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
    app.run(debug=True,host='0.0.0.0')
