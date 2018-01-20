#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2017/8/5 15:42
# @Author  : ILoveYz
# @File    : gradcaptcha.py

from PIL import Image
from bs4 import BeautifulSoup
import requests
import os
from time import sleep
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

os.chdir('folder')     # 改变目录

# captcha_url = 'http://192.168.240.168/xuanke/code.asp?id=!!!&random='   # 验证码地址
# captcha_url = 'http://192.168.240.168/xuanke/captcha.asp'   # 验证码地址
captcha_url = 'http://192.168.240.168/xuanke/code.asp'   # 验证码地址

infos = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.87 Safari/537.36'}
# infos = {'User-Agent':'Mozilla/4.0(compatible; MSIE 8.0; Windows NT 5.1;Trident/4.0; InfoPath.2; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'}
n = 1

while True:
    # res = requests.get(captcha_url,infos)
    res = requests.get(captcha_url,infos)
    fp = open('{}'.format(n) + '.png','wb')
    fp.write(res.content)
    fp.close()
    print n,'picture(s) is ok...'
    n += 1
    sleep(1)