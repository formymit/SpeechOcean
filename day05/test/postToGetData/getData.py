#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: getData.py 
@time: 2017/05/24 
"""
import requests
import re
from lxml import etree
import time
from mongodb_queue import MongoQueue
import multiprocessing


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0'
}

url = 'http://www.sonin.mn/content/page'
spider_queue = MongoQueue('mongolia', 'news_politics')


def infoCrawler():
    while True:
        try:
            page_id = spider_queue.pop()
            print(page_id)
        except KeyError:
            print('队列咩有数据')
            break
        else:
            getDataF1(page_id)
            spider_queue.complete(page_id)


def getDataF1(page_id):
    data = {
        'page_id':page_id, #"1",
        'catgegory_id':"1",#"8",#"9",
        'slug':"politics-economy",#"sport",#"easy-page"
    }

    response = requests.post(url, data=data)

    selector = etree.HTML(response.text)

    all_titles = selector.xpath('//a[@class="title"]')
    all_href = selector.xpath('//a[@class="title"]/@href')

    for i in range(len(all_titles)):
        title = all_titles[i].xpath('string(.)')
        href = all_href[i]
        href = 'http://www.sonin.mn' + href
        print(title + ', ' + href)
        with open('sport_urls.txt', 'a') as f:
            f.write(href + '\n')

def process_crawler():
    process= []
    # num_cpus = multiprocessing.cpu_count()
    # print('将启动进程数为: ', num_cpus)
    for i in range(40):
        p = multiprocessing.Process(target=infoCrawler)
        p.start()
        process.append(p)
    for p in process:
        p.join()

if __name__ == '__main__':
    process_crawler()
    # for i in range(56):
    #     getDataF1(i)
    #     time.sleep(1)
