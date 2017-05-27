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


url = 'http://dnn.mn/%D0%BC%D1%8D%D0%B4%D1%8D%D1%8D/%D1%83%D0%BB%D1%81-%D1%82%D3%A9%D1%80/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0'
}

spider_queue = MongoQueue('mongolia', 'dnn_url01')

def infoCrawler():
    while True:
        try:
            url = spider_queue.pop()
            print(url)
        except KeyError:
            print('队列没有数据啦')
            break
        else:
            result = getData(url)
            if len(result) == 0:
                spider_queue.reset(url)
            else:
                spider_queue.complete(url)


def getData(url):
    try:
        sumContent = ''

        response = requests.get(url, headers=headers)

        # print(response.encoding)

        selector = etree.HTML(response.text)

        all_titles = selector.xpath('//h1')
        title = all_titles[0].xpath('string(.)')

        all_time = selector.xpath('//div[@class="article_publish"]//span')
        time = all_time[0].xpath('string(.)')


        all_content = selector.xpath('//div[@class="article_content"]//p')  #默认第一个
        print(len(all_content))

        for i in range(len(all_content)):
            content = all_content[i].xpath('string(.)')
            content = ' '.join(content.split())
            content = '<p>' + content + '</p>'

            sumContent = sumContent + content
        review = ''
        # print(time + ', ' + title + ', \n' + sumContent )
        result = '{' + '"title": ' + '"' + title + '", ' + '"url": ' + '"' + url[:-1] + '", ' + '"review": ' + '"' + review + '", ' + '"content": ' + '"' + sumContent + '", ' + '"time": ' + '"' + time + '", ' + '"type": ' + '"news"' + '}'
        print(result)
        if len(title) > 1:  # there exist data
            with open('dnn_Data.txt', 'a') as file:
                file.write(result + '\n')

        # with open('mn_dnn01_urls.txt', 'a') as f:
        #         f.write(href + '\n')

    except Exception as e:
        print(e)
    return sumContent
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
    # getData('http://dnn.mn/%D0%B0%D0%BD-%D1%8B%D0%BD-%D2%AF%D0%B1%D1%85-%D0%BD%D1%8B-%D1%85%D1%83%D1%80%D0%B0%D0%BB%D1%82%D0%B0%D0%B9-%D1%85%D0%BE%D0%BB%D0%B1%D0%BE%D0%BE%D1%82%D0%BE%D0%B9%D0%B3%D0%BE%D0%BE%D1%80-%D1%83%D0%B8%D1%85-%D1%8B%D0%BD-%D2%AF%D0%B4%D1%8D%D1%8D%D1%81-%D1%85%D0%BE%D0%B9%D1%88%D1%85%D0%B8-%D1%87%D1%83%D1%83%D0%BB%D0%B3%D0%B0%D0%BD-%D1%85%D1%83%D1%80%D0%B0%D0%BB%D0%B4%D1%81%D0%B0%D0%BD%D0%B3%D2%AF%D0%B9/')
