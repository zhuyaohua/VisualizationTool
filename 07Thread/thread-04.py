"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     thread-04.py
@Author:   shenfan
@Time:     2022/9/28 13:54
"""
import threading
import time
import math

n = 100
m = 100
lock = threading.Lock()


class Mythread(threading.Thread):
    def __init__(self, func, *args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self) -> None:
        self.result = self.func(*self.args)




def add():
    global n
    lock.acquire()
    temp = n
    time.sleep(0.001)
    n = temp - 1
    lock.release()

def bfadd():
    start = time.time()
    threads = []
    for i in range(100):
        t = Mythread(add)
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    end = time.time()
    print("处理时间为：%s" % (end-start))


def adds():
    start = time.time()
    time.sleep(0.001)
    global m
    for i in range(100):
        m -= 1
    end = time.time()
    print("非并发处理时间为:%s" % (end-start))





adds()
bfadd()
print(n)
print(m)