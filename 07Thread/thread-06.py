"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     thread-06.py
@Author:   shenfan
@Time:     2022/9/29 14:01
"""
import threading
from datetime import datetime
import time


"""
   需求：
       1、A公布任务
       2、任务开始后（BCDEFG）执行
       3、A结束
       4、BCDEFG结束
    同步状态
"""


class Boss(threading.Thread):
    def run(self) -> None:
        print(event.isSet())
        event.set()
        print(self.name, "工作开始...(boss)!", datetime.now().strftime("%x %X.%f"))
        time.sleep(2)
        print(self.name, "工作完成...(boss)!", datetime.now().strftime("%x %X.%f"))
        event.set()


class Employer(threading.Thread):
    def run(self) -> None:
        event.wait()
        time.sleep(1)
        print(self.name, "悲催...(employer)!", datetime.now().strftime("%x %X.%f"))
        event.clear()
        event.wait()
        time.sleep(1)
        print(self.name, "高兴...(employer)!", datetime.now().strftime("%x %X.%f"))


if __name__ == "__main__":
    event = threading.Event()
    threads = []
    for i in range(5):
        t = Employer()
        threads.append(t)
    threads.append(Boss())
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("Ending...")


