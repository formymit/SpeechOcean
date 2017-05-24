#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: clearURLs.py 
@time: 2017/05/24 
"""

with open('mongolia_News_urls.txt', 'r') as f:
    data = f.readline()
    while data:
        if len(data) > len('http://www.mgyxw.net/am/2013/9/5/7246_143276.html?pid=1509') - 1:
            # http://www.mgyxw.net/am/2013/9/5/7246_143276.html?pid=1509
            # http://www.mgyxw.net/am/2015/5/7/U_6686_223693.html?pid=1453
            print(data)
            with open('urls.txt', 'a') as f2:
                f2.write(data)

        data = f.readline()