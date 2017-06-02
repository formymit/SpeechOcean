#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: mongoliaSpider.py 
@time: 2017/05/24 
"""
import requests
from lxml import etree
import time
from mongodb_queue import MongoQueue
import multiprocessing

# url = 'http://www.mgyxw.net/am/2013/8/1/U_6728_32320.html?pid=1467'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0'
}

spider_queue = MongoQueue('mongolia', 'news01')


def infoCrawler():
    while True:
        try:
            url = spider_queue.pop()
            print(url)
        except KeyError:
            print('队列咩有数据')
            break
        else:
            title = getData(url)
            spider_queue.complete(url)
            # if len(title) > 1:
            #     spider_queue.complete(url)
            # else:
            #     spider_queue.reset(url)

def getData(url):
    title = ''
    try:
        descriptions = ''

        response = requests.get(url, headers=headers)

        # print(response.encoding)
        response.encoding = 'utf-8'
        # print(response.text)

        selector = etree.HTML(response.text)

        all_titles = selector.xpath('//span[@id="ctl00_cph_lblTitle"]')
        all_times = selector.xpath('//div[@id="mkh_date"]')
        all_description = selector.xpath('//span[@id="ctl00_cph_Description"]//td')

        title = all_titles[0].xpath('string(.)')
        time = all_times[0].xpath('string(.)')
        review = ''


        # print(title)
        # print(time)

        for each in all_description:
            description = each.xpath('string(.)')
            descriptions = descriptions + description

        # print(descriptions)
        descriptions = ' '.join(descriptions.split())
        result = '{' + '"title": ' + '"' + title + '", '+ '"url": ' + '"' + url[:-1] + '", ' + '"review": ' + '"' + review + '", '+ '"content": ' + '"' + descriptions + '", '+ '"time": ' + '"' + time + '", ' + '"type": ' + '"news"'+ '}'
        print(result)

        if len(title) > 1: #there exist data
            with open('mongoliaData03.txt', 'a') as file:

                file.write(result + '\n')

    except Exception as e:
        print(e)

    return title


def process_crawler():
    process= []
    # num_cpus = multiprocessing.cpu_count()
    # print('将启动进程数为: ', num_cpus)
    for i in range(50):
        p = multiprocessing.Process(target=infoCrawler)
        p.start()
        process.append(p)
    for p in process:
        p.join()

if __name__ == "__main__":
    process_crawler()

    # getData('http://www.mgyxw.net/am/2016/12/12/U_9378_438169.html?pid=1991')
    # getData('http://www.mgyxw.net/am/2015/7/9/8955_226137.html?pid=1473')
    # getData('http://www.nmg.xinhuanet.com/mg/')

# getData(url)
#
# with open('test_urls', 'r') as f:
#     url = f.readline()
#     while url:
#         url = url[:-1]
#         print(url)
#         getData(url)
#         time.sleep(1)



#         url = f.readline()
