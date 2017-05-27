#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: geturls.py 
@time: 2017/05/27 
"""

#!usr/bin/env python3.6
#-*- coding:utf-8 -*-
"""
@author:iBoy
@file: getURLs.py
@time: 2017/05/26
"""
import requests
from lxml import etree
from mongodb_queue import MongoQueue
import multiprocessing


url = 'https://www.dorgio.mn/c/1'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0'
}

spider_queue = MongoQueue('mongolia', 'dorgio01')

def infoCrawler():
    while True:
        try:
            url = spider_queue.pop()
            print(url)
        except KeyError:
            print('队列没有数据啦')
            break
        else:
            getData(url)
            spider_queue.complete(url)


def getData(url):
    try:
        response = requests.get(url, headers=headers)

        # print(response.encoding)

        selector = etree.HTML(response.text)

        all_titles = selector.xpath('//h1[@class="fs16"]//a')
        all_hrefs = selector.xpath('//h1[@class="fs16"]//a/@href')

        for i in range(len(all_titles)):
            title = all_titles[i].xpath('string(.)')
            href = all_hrefs[i]


            print(title + ', ' + href)

            with open('dorgio_urls.txt', 'a') as f:
                f.write(href + '\n')
    except Exception as e:
        print(e)

def process_crawler():
    process = []
    for i in range(30):
        p = multiprocessing.Process(target=infoCrawler)
        p.start()
        process.append(p)
    for p in process:
        p.join()

if __name__ == '__main__':
    process_crawler()
    #
    # for i in range(1, 5):
    #     url = 'https://www.dorgio.mn/c/1?page=' + str(i)
    #     getData(url)
