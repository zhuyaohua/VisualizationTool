"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     example_dataset.py
@Author:   shenfan
@Time:     2022/9/21 14:07
"""
from sklearn import datasets


iris = datasets.load_iris()
digits = datasets.load_digits()

# print(iris)
print(digits.data)




