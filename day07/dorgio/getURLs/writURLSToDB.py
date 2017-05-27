#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: writURLSToDB.py 
@time: 2017/05/27 
"""
from  mongodb_queue import MongoQueue
spider_queue = MongoQueue('mongolia', 'dorgio01')

# def getOririn(url_tmp, total):
#     for i in range(1, int(total) + 1):
#
#         # url = 'https://www.dorgio.mn/c/1?page=' + str(i)
#         # url = 'https://www.dorgio.mn/c/2?page=' + str(i)
#         url =  url_tmp + str(i)
#         print(url)
#         with open('dorgio_origin_urls.txt', 'a') as f:
#             f.write(url + '\n')
         # spider_queue.push(url)

# https://www.dorgio.mn/c/2?page=787

# https://www.dorgio.mn/c/3?page=61
# https://www.dorgio.mn/c/5?page=10
# https://www.dorgio.mn/c/6?page=40
# https://www.dorgio.mn/c/9?page=131
# https://www.dorgio.mn/c/10?page=206
# https://www.dorgio.mn/c/11?page=629

# list = ['https://www.dorgio.mn/c/3?page=61', 'https://www.dorgio.mn/c/5?page=10', 'https://www.dorgio.mn/c/6?page=40',
#         'https://www.dorgio.mn/c/9?page=131', 'https://www.dorgio.mn/c/10?page=206', 'https://www.dorgio.mn/c/11?page=629']
#
# for each in list:
#     start = each.find('=')
#
#     total = each[start+1:]
#     url_tmp = each[:start+1]
#     getOririn(url_tmp, total)


with open('dorgio_origin_urls.txt', 'r') as f2:
    url = f2.readline()
    while url:
        try:
            spider_queue.push(url)
            url = f2.readline()
        except Exception as e:
            print(e)
