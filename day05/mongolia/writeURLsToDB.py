#-*- coding:utf-8 -*-
""" 
@author:iBoy 
@file: writeURLsToDB.py 
@time: 2017/05/22 
"""
from mongodb_queue import MongoQueue

spider_queue = MongoQueue('mongolia', 'news01')

with open('urls.txt') as f:
    data = f.readline()
    while data:
        spider_queue.push(data)
        print(data)
        data = f.readline()

