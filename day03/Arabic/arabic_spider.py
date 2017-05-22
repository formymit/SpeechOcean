#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: arabic_spider.py 
@time: 2017/05/22 
"""
import requests
from lxml import etree
import multiprocessing
from Download import request

from day01.Arabic.mongodb_queue import MongoQueue

# from pyquery import PyQuery as pq

spider_queue = MongoQueue('Arabic', 'Arabic_Crawl_queue')


def SingleProcessSpider():

    while True:
        try:
            url = spider_queue.pop()
        except KeyError:
            print('队列咩有数据')
            break
        else:
            getData(url)
            spider_queue.complete(url)

            #异常处理



# url = 'http://www.echoroukonline.com/ara/articles/1001.html'

def getData(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0'
    }

    response = request.get(url, 3)

    # print(response.encoding)

    response.encoding = 'utf-8'

    selector = etree.HTML(response.text)

    all_titles = selector.xpath('//h3[@class="main-title"]')
    all_reviews = selector.xpath('div[@class="comment-content"]//p')
    all_ps = selector.xpath('//section[@class="article-contents"]/p')
    all_contents = selector.xpath('//section[@class="article-contents"]/span')
    all_times = selector.xpath('//section[@class="article-text"]//div[@class="meta-m"]/span')

    #get title
    title = all_titles[0].xpath('string(.)')
    title = title.strip()

    print(title+ url)

    #get review
    sum_review = ''
    for each in all_reviews:
        review = each.xpath('string(.)')
        review = '<p>' + review + '</p>'
        # print(lable_p)
        sum_review = sum_review + review


    #get time
    time = all_times[0].xpath('string(.)')
    # print(time)

    #get content
    sum_content = ''

    #p label

    for each in all_ps:
        lable_p = each.xpath('string(.)')
        lable_p = '<p>' + lable_p + '</p>'
        # print(lable_p)
        sum_content = sum_content + lable_p


    #content
    for each in all_contents:
        content = each.xpath('string(.)')
        # content = content.replace('	', '')  #??

        # print(content)
        sum_content = sum_content + content

    sum_content = ''.join(sum_content.strip())
    sum_content = sum_content.replace('\n', ' ')
    # print(time, sum_content)

    with open('data.txt', 'a') as file:

        info = {
            'title': title,
            'url': url,
            'review': sum_review,
            'content': sum_content,
            'time': time,
            'type': 'news'
        }

        # print(info)

        file.write(str(info) + '\n')

    file.close()

def process_crawler():
    process= []
    # num_cpus = multiprocessing.cpu_count()
    # print('将启动进程数为: ', num_cpus)
    for i in range(30):
        p = multiprocessing.Process(target=SingleProcessSpider)
        p.start()
        process.append(p)
    for p in process:
        p.join()


if __name__ == '__main__':
    # getData(url)
    # SingleProcessSpider()

    process_crawler()



    # getData('http://www.echoroukonline.com/ara/articles/1019.html')