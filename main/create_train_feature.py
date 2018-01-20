#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2017/9/2 20:58
# @Author  : ILoveYz
# @File    : create_train_feature.py

from PIL import Image
import os
import glob

def get_feature(img):
    """
    获取指定图片的特征值,
    1. 按照每排的像素点,高度为19,则有19个维度,然后为13列,总共32个维度
    :param img_path:
    :return:一个维度为32（高度）的列表
    """
    width, height = img.size
    pixel_cnt_list = []
    for y in range(height):
        pix_cnt_x = 0
        for x in range(width):
            if img.getpixel((x, y)) == 0:  # 黑色点
                pix_cnt_x += 1

        pixel_cnt_list.append(pix_cnt_x)

    for x in range(width):
        pix_cnt_y = 0
        for y in range(height):
            if img.getpixel((x, y)) == 0:  # 黑色点
                pix_cnt_y += 1

        pixel_cnt_list.append(pix_cnt_y)

    return pixel_cnt_list

if __name__ == '__main__':
    # fp = open(u'D:/PycharmProjects/train_pix_feature.txt','w')
    fp = open(u'D:/PycharmProjects/test_pix_feature.txt','w')
    # N = 0
    # while N <= 9:
    #     root = u'D:/PycharmProjects/破解学校选课系统/imgs/cut_pic_{}/*.png'.format(N)
    #     pics = glob.glob(root)
    #     for p in pics:
    #         image = Image.open(p)
    #         plist = get_feature(image)
    #         n = 1
    #         fp.write('{}'.format(N))
    #         for pl in plist:
    #             fp.write(' %d:%d' % (n,pl))
    #             n += 1
    #         fp.write('\n')
    #     N += 1
    # fp.close()

    N = 0
    while N <= 0:
        # root = u'D:/PycharmProjects/破解学校选课系统/imgs/test_cut_pic_{}/*.jpg'.format(N)
        root = u'D:/PycharmProjects/cut_pic/*.png'
        pics = glob.glob(root)
        for p in pics:
            image = Image.open(p)
            plist = get_feature(image)
            n = 1
            fp.write('{}'.format(N))
            for pl in plist:
                fp.write(' %d:%d' % (n,pl))
                n += 1
            fp.write('\n')
        N += 1
    fp.close()