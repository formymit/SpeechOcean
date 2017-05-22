import json

from day01.Arabic.mongodb_queue import MongoQueue

spider_queue = MongoQueue('Arabic', 'Arabic_Crawl_queue')



#get the urls and writo to MongoDB
with open('/Users/iBoy/Desktop/Data/ar15_0.txt', 'r') as file:
    data = file.readline()
    while data:
        myjson = json.loads(data)
        print(myjson['url'])

        url = myjson['url']
        spider_queue.push(url)

        # with open('urlList.txt', 'a') as file2:
        #     file2.write(myjson['url'] + '\n')
        #     file2.close()


        data = file.readline()

