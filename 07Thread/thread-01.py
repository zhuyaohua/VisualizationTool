"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     thread-01.py
@Author:   shenfan
@Time:     2022/9/26 10:26
"""
import threading
import datetime
import time
from functools import wraps


def addstamptime(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("%s：时间戳为：%s" % (func.__name__, time.ctime()))
        func(*args, **kwargs)
        return func

    return wrapper


def threading01(num):
    print("%s>>> %d线程开始时间 \t%s" % (threading01.__name__, num, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")))
    time.sleep(5)
    print("%s结束" % threading01.__name__,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))


@addstamptime
def threading02(num):
    print("%s>>>%d开始时间 \t%s" % (threading02.__name__, num, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")))
    time.sleep(3)
    print("%s结束" % threading02.__name__, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))


if __name__ == "__main__":
    t1 = threading.Thread(target=threading01, args=(7,))
    t2 = threading.Thread(target=threading02.__wrapped__, args=(1,))
    threads = [t1, t2]
    print("ending...\t", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    # t1.setDaemon(True)
    for t in threads:
        print(threading.active_count())
        t.setDaemon(True)
        t.start()


