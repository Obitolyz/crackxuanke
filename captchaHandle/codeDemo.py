#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2017/9/2 23:40
# @Author  : ILoveYz
# @File    : main.py

from PIL import Image
from svmutil import *
import glob
import re
import time

# pics = glob.glob('D:/PycharmProjects/test_pics/*.jpg')
# pat = r'D:/PycharmProjects/test_pics\\(.*).jpg'

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

def get_bin_table(threshold=127):     # threshold 阈值
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    return table

def get_crop_imgs(img):     # 字符分割
    """
    按照图片的特点,进行切割,这个要根据具体的验证码来进行工作.
    :param img:
    :return:
    """
    # fp = open('D:/PycharmProjects/crack_captcha_feature.txt','w')
    model = svm_load_model('D:/PycharmProjects/train_results.txt')
    captcha = ''
    for i in range(6):
        x = i * 13  # 见原理图
        y = 0
        child_img = img.crop((x, y, x + 13, y + 19))
        # child_img.save('../cut_pic/{}.png'.format(i))
        # child_img.show()
        img_feature_list = get_feature(child_img)

        yt = [0]  # 测试数据标签
        # xt = [{1: 1, 2: 1}]  # 测试数据输入向量
        xt = convert_feature_to_vector(img_feature_list)  # 将所有的特征转化为标准化的SVM单行的特征向量
        p_label, p_acc, p_val = svm_predict(yt, xt, model,"-q")
        captcha += str(int(p_label[0]))

    return captcha

def convert_feature_to_vector(feature_list):
    """
    :param feature_list:
    :return:
    """
    index = 1
    xt_vector = []
    feature_dict = {}
    for item in feature_list:
        feature_dict[index] = item
        index += 1
    xt_vector.append(feature_dict)
    return xt_vector

def svm_model_test():
    """
    使用测试集测试模型
    :return:
    """
    yt, xt = svm_read_problem('D:/PycharmProjects/crack_captcha_feature.txt')
    model = svm_load_model('D:/PycharmProjects/train_results.txt')
    p_label, p_acc, p_val = svm_predict(yt, xt, model)       # p_label即为识别的结果

    for item in p_label:
        print '%d' % item,

def recognizeImgCode(pic):
    image = Image.open(pic).convert('L')  # 转化为灰度图
    # res = re.findall(pat, pic)[0]
    box = (26, 3, 26 + 78, 3 + 19)
    image = image.crop(box)  # 切割图片
    # image.show()
    # image.close()  # 先关闭文件才可以删除

    table = get_bin_table()
    image = image.point(table, '1')  # 二值化
    img_array = image.load()
    width, heigth = image.size
    # 去掉部分干扰线
    for h in range(heigth):
        for w in range(width):
            dot = img_array[w, h]
            if not dot:
                if (0 < h < heigth - 1) and (0 < w < width - 1):
                    if (img_array[w, h - 1] != 0) and (img_array[w, h + 1] == 1):
                        img_array[w, h] = 1
                else:
                    if w == 0 or w == width - 1:
                        if h == 0 or h == heigth - 1:
                            img_array[w, h] = 1
                        else:
                            if (img_array[w, h - 1] == 1) and (img_array[w, h + 1] == 1):
                                img_array[w, h] = 1
                    else:
                        if h == 0:
                            if img_array[w, h + 1] == 1:
                                img_array[w, h] = 1
                        if h == heigth - 1:
                            if img_array[w, h - 1] == 1:
                                img_array[w, h] = 1

    for h in range(1, heigth - 1):
        for w in range(1, width - 1):
            if (img_array[w - 1, h] == 1) and (img_array[w + 1, h] == 1):
                img_array[w, h] = 1

    for h in range(heigth):
        for w in range(width):
            dot = img_array[w, h]
            if not dot:
                if (0 < h < heigth - 1) and (0 < w < width - 1):
                    if (img_array[w, h - 1] != 0) and (img_array[w, h + 1] == 1):
                        img_array[w, h] = 1
                else:
                    if w == 0 or w == width - 1:
                        if h == 0 or h == heigth - 1:
                            img_array[w, h] = 1
                        else:
                            if (img_array[w, h - 1] == 1) and (img_array[w, h + 1] == 1):
                                img_array[w, h] = 1
                    else:
                        if h == 0:
                            if img_array[w, h + 1] == 1:
                                img_array[w, h] = 1
                        if h == heigth - 1:
                            if img_array[w, h - 1] == 1:
                                img_array[w, h] = 1

    # image.close()
    captcha = get_crop_imgs(image)
    return captcha

if __name__ == '__main__':
    time1 = time.time()
    # n = 1204
    # root = u'D:/PycharmProjects/破解学校选课系统/folder2/{}.jpg'
    # image = Image.open(root.format(n)).convert('L')    # 转化为灰度图
    # box = (26,3,26+78,3+19)
    # image = image.crop(box)     # 切割图片
    # # image.show()
    #
    # table = get_bin_table()
    # image = image.point(table,'1')            # 二值化
    # img_array = image.load()
    # width,heigth = image.size
    # # 去掉部分干扰线
    # for h in range(heigth):
    #     for w in range(width):
    #         dot = img_array[w,h]
    #         if not dot:
    #             if (0 < h < heigth-1) and (0 < w < width-1):
    #                 if (img_array[w,h-1] != 0) and (img_array[w,h+1] == 1):
    #                     img_array[w,h] = 1
    #             else:
    #                 if w == 0 or w == width -1:
    #                     if h == 0 or h == heigth-1:
    #                         img_array[w,h] = 1
    #                     else:
    #                         if (img_array[w, h - 1] == 1) and (img_array[w, h + 1] == 1):
    #                             img_array[w, h] = 1
    #                 else:
    #                     if h == 0:
    #                         if img_array[w,h+1] == 1:
    #                             img_array[w,h] = 1
    #                     if h == heigth-1:
    #                         if img_array[w,h-1] == 1:
    #                             img_array[w,h] = 1
    #
    # for h in range(1,heigth-1):
    #     for w in range(1,width-1):
    #         if (img_array[w-1,h] == 1) and (img_array[w+1,h] == 1):
    #             img_array[w,h] = 1
    #
    # for h in range(heigth):
    #     for w in range(width):
    #         dot = img_array[w,h]
    #         if not dot:
    #             if (0 < h < heigth-1) and (0 < w < width-1):
    #                 if (img_array[w,h-1] != 0) and (img_array[w,h+1] == 1):
    #                     img_array[w,h] = 1
    #             else:
    #                 if w == 0 or w == width -1:
    #                     if h == 0 or h == heigth-1:
    #                         img_array[w,h] = 1
    #                     else:
    #                         if (img_array[w, h - 1] == 1) and (img_array[w, h + 1] == 1):
    #                             img_array[w, h] = 1
    #                 else:
    #                     if h == 0:
    #                         if img_array[w,h+1] == 1:
    #                             img_array[w,h] = 1
    #                     if h == heigth-1:
    #                         if img_array[w,h-1] == 1:
    #                             img_array[w,h] = 1
    #
    # # image.show()
    # get_crop_imgs(image)
    # # svm_model_test()
    tot = 0
    for pic in pics:
        image = Image.open(pic).convert('L')    # 转化为灰度图
        res = re.findall(pat,pic)[0]
        box = (26,3,26+78,3+19)
        image = image.crop(box)     # 切割图片
        # image.show()

        table = get_bin_table()
        image = image.point(table,'1')            # 二值化
        img_array = image.load()
        width,heigth = image.size
        # 去掉部分干扰线
        for h in range(heigth):
            for w in range(width):
                dot = img_array[w,h]
                if not dot:
                    if (0 < h < heigth-1) and (0 < w < width-1):
                        if (img_array[w,h-1] != 0) and (img_array[w,h+1] == 1):
                            img_array[w,h] = 1
                    else:
                        if w == 0 or w == width -1:
                            if h == 0 or h == heigth-1:
                                img_array[w,h] = 1
                            else:
                                if (img_array[w, h - 1] == 1) and (img_array[w, h + 1] == 1):
                                    img_array[w, h] = 1
                        else:
                            if h == 0:
                                if img_array[w,h+1] == 1:
                                    img_array[w,h] = 1
                            if h == heigth-1:
                                if img_array[w,h-1] == 1:
                                    img_array[w,h] = 1

        for h in range(1,heigth-1):
            for w in range(1,width-1):
                if (img_array[w-1,h] == 1) and (img_array[w+1,h] == 1):
                    img_array[w,h] = 1

        for h in range(heigth):
            for w in range(width):
                dot = img_array[w,h]
                if not dot:
                    if (0 < h < heigth-1) and (0 < w < width-1):
                        if (img_array[w,h-1] != 0) and (img_array[w,h+1] == 1):
                            img_array[w,h] = 1
                    else:
                        if w == 0 or w == width -1:
                            if h == 0 or h == heigth-1:
                                img_array[w,h] = 1
                            else:
                                if (img_array[w, h - 1] == 1) and (img_array[w, h + 1] == 1):
                                    img_array[w, h] = 1
                        else:
                            if h == 0:
                                if img_array[w,h+1] == 1:
                                    img_array[w,h] = 1
                            if h == heigth-1:
                                if img_array[w,h-1] == 1:
                                    img_array[w,h] = 1

        # image.show()
        captcha = get_crop_imgs(image)
        # print captcha,res
        if captcha == res:
            tot += 1
        # svm_model_test()
    time2 = time.time()
    print time2 - time1
    print '验证码总数是:%d' % len(pics)
    print '识别成功:%d' % tot
    print '准确率:%.1f%%' % ((tot*1.0/len(pics))*100)