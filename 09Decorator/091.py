"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     091.py
@Author:   shenfan
@Time:     2022/9/23 11:09
"""
import pandas
import numpy
import matplotlib
import seaborn
from functools import wraps


def docdecretor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print("标准正太分布")
        return result
    return wrapper

@docdecretor
def normal_distribution(n):
    source = numpy.random.normal(size=n)
    seaborn.displot(source)
    matplotlib.pyplot.show()
    return source


normal_distribution(1000)
