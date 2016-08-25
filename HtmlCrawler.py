"""
HtmlCrawler class

When getting data from webpage, use HtmlCrawler
it uses BeautifulSoup to find tag, class, id and etc.
"""

#-*- coding: utf-8 -*-
__author__ = 'eric shin'

import BaseCrawler
from bs4 import BeautifulSoup

class HtmlCrawler(BaseCrawler.BaseCrawler):
	def getBs(self):
		soup = None
        
		try:
			data = BaseCrawler.BaseCrawler.getData(self)
			soup = BeautifulSoup(data, "html.parser", from_encoding="utf-8")
		except BaseCrawler.CrawlerException, e:
			raise BaseCrawler.CrawlerException(e)

		return soup

	
