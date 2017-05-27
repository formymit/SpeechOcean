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



headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0'
}

spider_queue = MongoQueue('mongolia', 'dorgio_urls')

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
            if len(result) == 0:  #很聪明的办法 用title代替 sumContent
                #区分没有抓到数据以及本身没有数据 有重置 死循环？ 谨慎重置 不然就是死循环 永远抓不完 如果有isotime 则complete
                spider_queue.reset(url)
            else:
                spider_queue.complete(url)


def getData(url):
    try:
        sumContent = ''

        response = requests.get(url, headers=headers)

        # print(response.encoding)

        selector = etree.HTML(response.text)

        all_titles = selector.xpath('//h1[@class="oranienbaum"]')
        title = all_titles[0].xpath('string(.)')

        all_time = selector.xpath('//span[@class="text-muted"]')
        time = all_time[0].xpath('string(.)')


        all_content = selector.xpath('//div[@class="post-content"]//p')  #默认第一个

        for i in range(len(all_content)):
            content = all_content[i].xpath('string(.)')
            content = ' '.join(content.split())
            content = '<p>' + content + '</p>'

            sumContent = sumContent + content

        all_review = selector.xpath('//ul[@id="comments"]//p')
        sum_Review = ''
        for i in range(len(all_review)):
            review = all_review[i].xpath('string(.)')
            review = ' '.join(review.split())
            review = '<p>' + review + '</p>'

            sum_Review = sum_Review + review
        # print(time + ', ' + title + ', \n' + sumContent )
        result = '{' + '"title": ' + '"' + title + '", ' + '"url": ' + '"' + url[:-1] + '", ' + '"review": ' + '"' + sum_Review + '", ' + '"content": ' + '"' + sumContent + '", ' + '"time": ' + '"' + time + '", ' + '"type": ' + '"news"' + '}'
        print(result)
        print(sumContent)
        print(len(sumContent))
        if len(sumContent) > 8:  # there exist data  <p></p>
            with open('dorgio_Data.txt', 'a') as file:
                file.write(result + '\n')

        # with open('mn_dnn01_urls.txt', 'a') as f:
        #         f.write(href + '\n')

    except Exception as e:
        print(e)
    return title
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
    # getData('https://www.dorgio.mn/p/71263')