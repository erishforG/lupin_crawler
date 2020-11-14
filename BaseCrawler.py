"""
BaseCrawler class

Each crawler has the same way to get data.
BaseCrawler uses urllib2 library to get data and returns string data encoded with UTF-8.
"""

#-*- coding: utf-8 -*-
__author__ = 'eric shin'

import re
import urllib.request
import time, threading
import socket
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class CrawlerException(Exception):
    pass


class BaseCrawler:
    url = ''
    def __init__(self, url):
        self.url = url

    def getData(self):
        req = urllib.request.Request(self.url)
        req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
        req.add_header("Accept-Language", "ko-KR,ko;")
        req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36")

        data = ''

        try:
            response = urllib.request.urlopen(req, None, 60)
            data = response.read()

        except Exception as e:
            raise CrawlerException(e)

        return data

    def getDataByBrowser(self):
        browser = webdriver.Chrome('/Users/erish/Documents/lupin_crawler/chromedriver')
        browser.implicitly_wait(3)
        browser.get(self.url)
        time.sleep(5) # 접속하는 동안 대기
        return browser.page_source