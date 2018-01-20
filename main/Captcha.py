#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PIL import Image
from bs4 import BeautifulSoup
import re
import requests
import os
import sys
from time import sleep,time
import codeDemo
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

# os.mkdir('folder')
os.chdir('folder')     # 改变目录

# 贼气，搞了这么久，就是因为login_url搞错了。。。
login_url = 'http://192.168.240.168/xuanke/entrance1.asp'  # 登录地址
# captcha_url = 'http://192.168.240.168/xuanke/code.asp?id=!!!&random='   # 验证码地址
captcha_url = 'http://192.168.240.168/xuanke/captcha.asp'   # 验证码地址
main_url = 'http://192.168.240.168/xuanke/edu_main.asp?xq=20171'
get_schedule_url = 'http://192.168.240.168/xuanke/get_schedule.asp?'     # 课程表ajax加载的地址
grad_class_url = 'http://192.168.240.168/xuanke/coursehtm/d3320171.htm'  # 信息工程学院的课
check_url = 'http://192.168.240.168/xuanke/sele_count1.asp?course_no=%s' # % 'course_no'  # 课程号

# 选课链接
xuanke_url = 'http://192.168.240.168/xuanke/choosecheck.asp?stu_no=test&no_type=%s'
# 确定选课的验证码地址
confirmcode_url = 'http://192.168.240.168/xuanke/code.asp'
# 确定选课验证码提交链接:
# submit_url = 'http://192.168.240.168/xuanke/choose.asp?GetCode=%s&no_type=1303130002 选修&submit=确    定'
submit_url = 'http://192.168.240.168/xuanke/choose.asp?GetCode={}&no_type=1303130002+%D1%A1%D0%DE&submit=%C8%B7++++%B6%A8'
# 必修: %B1%D8%D0%DE
# 选修: %D1%A1%D0%DE

infos = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.87 Safari/537.36'}

def LoginToXuanKe():
    session = requests.Session()
    respone = session.get(captcha_url,headers=infos)
    # cookies = {c.name : c.value for c in respone.cookies}
    # print cookies
    # cookies = ''
    # for index, cookie in enumerate(respone.cookies):
    #     cookies = cookies + cookie.name + "=" + cookie.value + ";"
    # cookie = cookies[:-1]

    fp = open('captcha' + '.png','wb')
    fp.write(respone.content)
    fp.close()
    # sid = raw_input('请输入的学号：')
    # password = raw_input('请输入密码：')
    # image = Image.open('captcha.png')
    # image.show()
    # captcha = raw_input('请输入验证码:')
    # image.close()        # 先关闭文件才可以删除
    # os.remove('captcha.png')   # 删除验证码
    captcha = codeDemo.recognizeImgCode('captcha.png')
    os.remove('captcha.png')   # 删除验证码


    postData = {
        'stu_no':'*********',   #sid,
        'passwd':'*********',
        'GetCode':captcha
    }
    Head = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Content-Length':'24',
        'Content-Type':'application/x-www-form-urlencoded',
        # 'Cookie':cookie,        # 不加cookie也是可以的,session自动管理
        'Host':'192.168.240.168',
        'Origin':'http://192.168.240.168',
        # 'Referer':'http://192.168.240.168/xuanke/edu_login.asp',#?msg=%D1%E9%D6%A4%C2%EB%CA%E4%C8%EB%B4%ED%CE%F3%A3%AC%C7%EB%D6%D8%CA%E4%C8%EB!',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    r = session.post(url=login_url,data=postData)
    # print r.cookies
    # print r.content.decode('gb2312').encode('utf-8')
    #　没有post成功
    # respone = session.get(get_schedule_url,headers=infos)
    # html = respone.content.decode('gb2312').encode('utf-8')
    if r.content[0] == '<':
        print '登录失败...'
        return 'N'
    # soup = BeautifulSoup(html,"html.parser")
    # # print soup.prettify()
    # classes = soup.find_all('td',attrs={"rowspan":"2"})
    # for cs in classes:
    #     print cs.text      # 如果是string的话,含有<br>匹配不了    text就可以了

    return 'Y',session

if __name__ == '__main__':
    time1 = time()
    pat = "<br>主选学生限制人数：(.*)&nbsp;&nbsp;主选学生已选人数：(.*)<br>"
    while True:
        flag = LoginToXuanKe()
        if flag == 'N':
            continue
        else:
            session = flag[1]
            response = session.get(check_url % '1303130002',headers=infos)
            html = response.content.decode('gb2312').encode('utf-8')
            # print html
            res = re.findall(pat,html)
            # print res
            time2 = time()
            print time2 - time1
            if res:
                nbr = res[0]
                if int(nbr[0]) > int(nbr[1]):
                    print '这课还有%d个位置...' % (int(nbr[0])-int(nbr[1]))
                    session.get(xuanke_url % '1303130002+选修',headers=infos)
                    pic = session.get(confirmcode_url,headers=infos)
                    fp = open('captcha' + '.png', 'wb')
                    fp.write(pic.content)
                    fp.close()
                    image = Image.open('captcha.png')
                    image.show()
                    captcha = raw_input('请输入验证码:')
                    print captcha
                    image.close()
                    os.remove('captcha.png')
                    response = session.get(submit_url.format(captcha),headers=infos)
                    # print response.content.decode('gb2312').encode('utf-8')
                    print response.content.decode('gbk').encode('utf-8')
                else:
                    print '很遗憾,这课没有位置了...'
            print '登录成功...'
            # 退出登录
            session.get('http://192.168.240.168/xuanke/exit.asp',headers=infos)
            break
