"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     thread-03.py
@Author:   shenfan
@Time:     2022/9/27 10:30
"""
import threading
from datetime import datetime
import sys

sys.setrecursionlimit(10000)


def sum(n):
    if n > 1:
        return n + sum(n - 1)
    if n == 1:
        return n


def product(n):
    if n > 1:
        return n * product(n - 1)
    if n == 1:
        return n

def product1(n):
    res = 1
    for i in range(1,n+1):
        res = res*i
    return res



class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.args = args
        self.func = func

    def run(self):
        start = datetime.now()
        print("开始时间：%s" % start.strftime("%x %X.%f"))
        self.result = self.func(*self.args)
        end = datetime.now()
        print("处理结果：%s" % self.result)
        print("处理时间：%s" % (end-start))

    def getresult(self):
        return self.result


# t1 = MyThread(sum, (1000,))
# t2 = MyThread(product, (100000,))
t3 = MyThread(product1, (1000,))
# t1.start()
# t2.start()
t3.start()

