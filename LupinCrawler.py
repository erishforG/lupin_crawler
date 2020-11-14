"""
Main class

When starting, LupinCrawler send 'start message' into your messanger.
And then the crawler checks difference of webtoon sites / before and now.
If there is any difference, the crawler send 'new webtoon message' into your messanger.
"""

#-*- coding: utf-8 -*-
__author__ = 'eric shin'

import time
import sys, inspect
from threading import Thread
import os
import Crawlers
from http.client import BadStatusLine
import json
import requests
import datetime
import traceback
from difflib import SequenceMatcher

#slack library
#from slacker import Slacker

class LupinCrawler(Thread):  
    channel = '#lupin_crawler'
    check_time = 0

    def __init__(self):
        Thread.__init__(self)
        #send start message

    def run(self):
        self.data = {}
        
        for i in range(0, len(self.crawlers)):
            self.data[i] = ''

        while(True):
            for i in range(0, len(self.crawlers)):
                crawler = self.crawlers[i]

                try:
                    #get each crawler's site data
                    data = crawler.get()

                    #if there is any difference
                    if not ''.join(data)  == self.data[i]:
                        #if it is not the time of initialization
                        if not self.data[i] == '':
                            #send new webtoon message
                            print (data[0:200])

                    self.data[i] = ''.join(data)
                except Exception as e:
                    #if there is any crash, reset the crawler's data
                    self.data[i] = ''
    
                    #print log
                    print (crawler.url)
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                    print (''.join('* ' + line for line in lines))

            now = datetime.datetime.now()

            #check crawlers work fine each 12 hour
            if int(now.hour) % 12 == 0 and self.check_time != now.hour :
                self.check_time = int(now.hour)
                    
                count = 0
                none_work_list = ''

                for i in range(0, len(self.crawlers)):
                    crawler = self.crawlers[i]
                    if self.data[i] == '':
                        count = count + 1
                        none_work_list += crawler.__class__.__name__ + '\n'
                    
                payload = {
                    "body" : self.channel + " is alive!",
                    "connectColor" : "#FAC11B",
                    "connectInfo" : [{
                        "title" : self.channel,
                        "description" : str(count) + " crawlers are not working!\n"
                            + none_work_list
                    }]
                }

                result = requests.post(self.jandi_url, data=json.dumps(payload), headers=self.jandi_header)

            time.sleep(3600)


    def start(self):
        Thread.start(self)

    def stop(self):
        pass

    def loadCrawlers(self):
        print ('importCrawlers')

        self.crawlers = []

        for name, obj in inspect.getmembers(Crawlers):
            if name == 'BaseCrawler':
                continue
            if name == 'HtmlCrawler':
                continue
            if inspect.isclass(obj):
                print (name)
                clazz = getattr(Crawlers, name)
                self.crawlers.append(clazz())

#initialization
if __name__ == "__main__":
    monitor = LupinCrawler()

    monitor.loadCrawlers()

    monitor.start()
