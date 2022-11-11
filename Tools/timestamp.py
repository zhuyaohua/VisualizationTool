"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     timestamp.py
@Author:   shenfan
@Time:     2022/11/11 15:24
"""
from datetime import datetime, timedelta
import time


def timestampList(days=False, hours=False, minute=False, length=0):
    now_time = datetime.now()
    times = []
    if days:
        for i in range(length):
            dt = (now_time - timedelta(days=i)).strftime("%Y-%m-%d %X")
            timestamp = time.mktime(time.strptime(dt, "%Y-%m-%d %X"))
            times.append((dt, int(timestamp)))
    if hours:
        for i in range(length):
            dt = (now_time - timedelta(hours=i)).strftime("%Y-%m-%d %X")
            timestamp = time.mktime(time.strptime(dt, "%Y-%m-%d %X"))
            times.append((dt, int(timestamp)))
    if minute:
        for i in range(length):
            dt = (now_time - timedelta(minutes=i)).strftime("%Y-%m-%d %X")
            timestamp = time.mktime(time.strptime(dt, "%Y-%m-%d %X"))
            times.append((dt, int(timestamp)))

    times.sort()
    for item in times:
        print(item)


timestampList(days=True, length=10)
