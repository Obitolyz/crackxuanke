#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2017/9/2 21:32
# @Author  : ILoveYz
# @File    : model_train.py

from svmutil import *

def train_svm_model():
    """
    训练并生成model文件
    :return:
    """
    y, x = svm_read_problem('D:/PycharmProjects/train_pix_feature.txt')
    model = svm_train(y, x)
    svm_save_model('D:/PycharmProjects/train_results.txt', model)

if __name__ == '__main__':
    train_svm_model()