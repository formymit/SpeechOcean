#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: getContent.py
@time: 2017/05/25
"""

import requests
from lxml import etree
from mongodb_queue import MongoQueue
import multiprocessing
import re

url = 'http://www.montsame.mn/read/55572'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0'
}

spider_queue = MongoQueue('mongolia', 'montsame_urls')


def infoCrawler():
    while True:
        try:
            url = spider_queue.pop()
            print(url)
        except KeyError:
            print('队列咩有数据')
            break
        else:
            getData(url)
            spider_queue.complete(url)

def getData(url):
    try:
        response = requests.get(url, headers=headers)


        selector = etree.HTML(str(response.text))

        title = selector.xpath('//h3[@class="news-title"]')[0].xpath('string(.)')
        # print(title)

        time = selector.xpath('//div[@class="info-bar pull-left"]//span')[0].xpath('string(.)')
        time = ' '.join(time.split())
        # print(time)

        all_content = selector.xpath('//div[@class="body"]//p')

        if len(all_content) == 0:
            all_content = selector.xpath('//div[@class="body"]')

        sumContent = ''
        for i in range(len(all_content)):
            content = all_content[i].xpath('string(.)')
            content = ' '.join(content.split())
            content = '<p>' + content + '</p>'
            sumContent = sumContent + content



        review = ''
        result = '{' + '"title": ' + '"' + title + '", ' + '"url": ' + '"' + url + '", ' + '"review": ' + '"' + review + '", ' + '"content": ' + '"' + sumContent + '", ' + '"time": ' + '"' + time + '", ' + '"type": ' + '"news"' + '}'
        print(result)

        if len(title) > 1: #there exist data
            with open('caakNewsData.txt', 'a') as file:

                file.write(result + '\n')

    except Exception as e:
        print(e)

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
    # getData('http://www.montsame.mn/read/54429')