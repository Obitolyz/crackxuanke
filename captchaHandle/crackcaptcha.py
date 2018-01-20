#!/usr/bin/env python
# -*- coding=utf-8 -*-

from PIL import Image
from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
import re
from time import sleep

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
pattern = "code.asp\?id=!!!&random=(.*)"
Head = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Host':'hm.baidu.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}
# os.chdir('folder')     # 改变目录

driver = webdriver.PhantomJS(executable_path='D:/phantomjs/bin/phantomjs')
while True:
    try:
        driver.get('http://192.168.240.168/xuanke/edu_login.asp')
        respone = driver.page_source     #.decode('gbk')

        soup = BeautifulSoup(respone,'html.parser')
        res = soup.select('img')[0]['src']
        # res = "code.asp?id=!!!&random=0.5218559638597071"
        rand = re.findall(pattern,res)
        print 'ok1...'
        if rand:
            fp = open('D:/PycharmProjects/破解学校选课系统/folder/' + '%s' % rand[0] + '.jpg','wb')
            respone = requests.get('http://192.168.240.168/xuanke/' + res)
            fp.write(respone.content)
            fp.close()
            print 'ok2...'
        sleep(0.5)
    except Exception:
        driver.quit()

# print respone