from mongodb_queue import MongoQueue

spider_queue = MongoQueue('mongolia', 'montsame_urls')

with open('montsame_urls.txt') as f:
    data = f.readline()
    while data:
        spider_queue.push(data[:-1])
        print(data[:-1])
        data = f.readline()