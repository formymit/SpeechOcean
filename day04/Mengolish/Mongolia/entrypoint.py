#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: entrypoint.py 
@time: 2017/05/23 
"""
from scrapy.cmdline import execute
execute(['scrapy', 'crawl', 'mongolia'])