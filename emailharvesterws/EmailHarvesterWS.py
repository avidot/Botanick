# -*- coding: utf-8 -*-

import _thread
import threading
import time
import subprocess
import os
from flask import Flask
import glob

class myThread (threading.Thread):
    def __init__(self, domain, engine):
        threading.Thread.__init__(self)
        self.domain = domain
        self.engine = engine
    def run(self):
        callEmailHarvester(self.domain, self.engine)
        
def callEmailHarvester(domain,engine):
    result = subprocess.call('emailharvester -d '+domain+' -e '+engine+' -s result_'+engine+'.txt', shell=True)
    

app = Flask(__name__)

def search2(domain):
    return "test"

@app.route('/domain=<domain>')
def search(domain):
    threads = []

    # Create new threads
    thread1 = myThread(domain, "google")
    thread2 = myThread(domain, "linkedin")
    thread3 = myThread(domain, "bing")
    thread4 = myThread(domain, "yahoo")
    thread5 = myThread(domain, "github")

    # Start new Threads
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    
    # Add threads to thread list
    threads.append(thread1)
    threads.append(thread2)

    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    list_of_files = glob.glob('./result_*.txt')
    emails_found=""
    for file_name in list_of_files:
        with open(file_name) as f:
            for line in f:
                if line not in emails_found:
                    if emails_found == "":
                        emails_found=line
                    else:
                        emails_found=emails_found+", "+line
        os.remove(file_name)

    return emails_found

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
