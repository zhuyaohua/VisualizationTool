"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     thread-02.py
@Author:   shenfan
@Time:     2022/9/26 15:32
"""
import threading
from datetime import datetime


class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args


    def run(self,):
        self.result = self.func(*self.args)
        print("%s running: started time is %s and result is %s" % (
            self.getName(), datetime.now().strftime("%x %X.%f"), self.result))

    def getresult(self):
        return self.result


if __name__ == "__main__":
    def count(n):
        return n ** 3


    t1 = MyThread(count, (1,))
    t2 = MyThread(count, (2,))
    t1.start()
    t2.start()
    print()
    print(t1.getresult())
