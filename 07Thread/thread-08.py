"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     thread-08.py
@Author:   shenfan
@Time:     2022/9/29 14:44
"""
"""
   需求： 最快不断去除一个list中的最后一个元素
"""

import numpy
import time
import queue


numpy.random.seed(1000)
data = list(numpy.random.rand(100))


def commfunc():
    start = time.time()
    for i in range(len(data)):
        data.pop(-1)
    end = time.time()
    print("处理时间：", end-start)


def multithread():
    fifo = queue.Queue()
    lifo = queue.LifoQueue()
    pri = queue.PriorityQueue()
    fifo.put(data)
    print(fifo.get())

commfunc()