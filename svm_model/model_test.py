#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2017/9/2 21:43
# @Author  : ILoveYz
# @File    : model_test.py

from svmutil import *

def svm_model_test():
    """
    使用测试集测试模型
    :return:
    """
    yt, xt = svm_read_problem('D:/PycharmProjects/test_pix_feature.txt')
    model = svm_load_model('D:/PycharmProjects/train_results.txt')
    p_label, p_acc, p_val = svm_predict(yt, xt, model)       # p_label即为识别的结果

    for item in p_label:
        print '%d ' % item,

if __name__ == '__main__':
    svm_model_test()