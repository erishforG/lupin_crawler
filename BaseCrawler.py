"""
BaseCrawler class

Each crawler has the same way to get data.
BaseCrawler uses urllib2 library to get data and returns string data encoded with UTF-8.
"""

#-*- coding: utf-8 -*-
__author__ = 'eric shin'

import re
import urllib2
import time, threading
import socket

class CrawlerException(Exception):
    pass


class BaseCrawler:
    url = ''
    def __init__(self, url):
        self.url = url

    def getData(self):
        req = urllib2.Request(self.url)
        req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
        req.add_header("Accept-Language", "ko-KR,ko;")
        req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36")

        data = ''

        try:
            response = urllib2.urlopen(req, None, 60)

            for line in response:
                data += line

        except Exception, e:
            raise CrawlerException(e)

        return data
