"""
Crawler list class

When listing each websites or any other urls to get any webtoon information, list up Crawlers.py.
You have to initialize each Crawler with name and you have to choose which way to get data like HtmlCrawler or BaseCrawler.
And then the class returns new webtoon list.
"""

#-*- coding: utf-8 -*-
__author__ = 'eric shin'

from BaseCrawler import BaseCrawler
from HtmlCrawler import HtmlCrawler
import datetime

class NaverCrawler(HtmlCrawler):
    def __init__(self):
        HtmlCrawler.__init__(self, 'http://comic.naver.com/webtoon/weekday.nhn')

    def get(self):
        soup = HtmlCrawler.getBs(self)
        
        data = soup.findAll(class_ = "thumb")
        
        result = []
        
        for object in data:
            if object.find(class_ = "ico_updt") is not None:
                result.append(object.img["title"] + " / " + self.url + object.a["href"])
        
        return result
