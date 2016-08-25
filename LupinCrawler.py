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
import urllib2
from httplib import BadStatusLine
import json
import requests
import datetime
import traceback
from difflib import SequenceMatcher

#slack library
#from slacker import Slacker

class LupinCrawler(Thread):
    # jandi / insert your jandi address
    jandi_url = ''
    
    jandi_header = {
    'Accept': 'application/vnd.tosslab.jandi-v2+json',
    'Content-Type': 'application/json'
    }
    
    channel = '#lupin_crawler'
    check_time = 0

    def __init__(self):
        Thread.__init__(self)

        #send start message
        #jandi
        payload = {
            "body" : self.channel + " start",
            "connectColor" : "#FAC11B",
            "connectInfo" : [{
                "title" : self.channel,
                "description" : self.channel + " start"
            }]
        }
 
        result = requests.post(self.jandi_url, data=json.dumps(payload), headers=self.jandi_header)

        #slack / insert your slack address
        #self.slack = Slacker('')
        #self.slack.chat.post_message(self.channel, 'start')

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
                            #jandi
                            payload = {
                                "body" : crawler.__class__.__name__ + " new webtoon arrived!",
                                "connectColor" : "#FAC11B",
                                "connectInfo" : [{
                                    "title" : self.channel,
                                    "description" : 
                                        "crawler name : " + crawler.__class__.__name__ + '\n'
                                        "crawler webtoon list : " + '\n' +
                                                 '\n'.join(data)
                                }]
                            }
                            
                            result = requests.post(self.jandi_url, data=json.dumps(payload), headers=self.jandi_header)

                            #slack
                            #self.slack.chat.post_message(self.channel, crawler.url + '\n' + '\n'.join(data))
                            
                            print data[0:200]

                    self.data[i] = ''.join(data)
                except Exception, e:
                    #if there is any crash, reset the crawler's data
                    self.data[i] = ''
    
                    #print log
                    print crawler.url
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                    print ''.join('* ' + line for line in lines)

            now = datetime.datetime.now();

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

            time.sleep(3)


    def start(self):
        Thread.start(self)

    def stop(self):
        pass

    def loadCrawlers(self):
        print('importCrawlers')

        self.crawlers = []

        for name, obj in inspect.getmembers(Crawlers):
            if name == 'BaseCrawler':
                continue
            if name == 'HtmlCrawler':
                continue
            if inspect.isclass(obj):
                print name
                clazz = getattr(Crawlers, name)
                self.crawlers.append(clazz())

    def my_import(self, name):
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

#initialization
if __name__ == "__main__":
    monitor = LupinCrawler()

    monitor.loadCrawlers()

    monitor.start()
