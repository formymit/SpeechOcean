#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: mongolia.py 
@time: 2017/05/23 
"""

from scrapy.spiders import CrawlSpider, Rule, Request ##CrawlSpider与Rule配合使用可以骑到历遍全站的作用、Request干啥的我就不解释了
from scrapy.linkextractors import LinkExtractor ##配合Rule进行URL规则匹配
# from items import MongoliaItem
from scrapy import FormRequest ##Scrapy中用作登录使用的一个包

class mySpider(CrawlSpider):
    name = 'mongolia'
    allowed_domains = ['mgyxw.net']
    # allowed_domains = ['nmg.xinhuanet.com']
    # allowed_domains = ['mongoliansti.com']

    start_urls = ['http://www.mgyxw.net/U_index.html']
    # start_urls = ['http://www.nmg.xinhuanet.com/mg/']
    # start_urls = ['http://mongolian.news.cn']
    # start_urls = ['http://www.mongoliansti.com']

    rules = (
        Rule(LinkExtractor(allow=('\.html',)), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(response.url)
        with open('mongolia_News_urls02.txt', 'a') as f:
            f.write(response.url+ '\n')
        pass