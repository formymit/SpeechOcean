#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: writePage_idToDB.py 
@time: 2017/05/25 
"""
from mongodb_queue import MongoQueue

spider_queue = MongoQueue('mongolia', 'news_politics')

for i in range(5485):
    spider_queue.push(i)

# with open('urls.txt') as f:
#     data = f.readline()
#     while data:
#         spider_queue.push(data)
#         print(data)
#         data = f.readline()
