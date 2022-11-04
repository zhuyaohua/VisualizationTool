"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     thread-05.py
@Author:   shenfan
@Time:     2022/9/28 15:05
"""
import threading
import time
"""
递归锁
"""


class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def actionA(self):
        lockr.acquire()
        print(self.name,"gotA",time.ctime())
        time.sleep(2)

        lockr.acquire()
        print(self.name,"gotB",time.ctime())
        time.sleep(2)

        lockr.release()
        lockr.release()

    def actionB(self):
        lockr.acquire()
        print(self.name,"gotB",time.ctime())
        time.sleep(2)

        lockr.acquire()
        print(self.name,"gotA",time.ctime())
        time.sleep(2)

        lockr.release()
        lockr.release()


    def run(self) -> None:
        self.actionA()
        self.actionB()


if __name__ == "__main__":
    lock1 = threading.Lock()
    lock2 = threading.Lock()
    lockr = threading.RLock()

    threads = []

    for i in range(5):
        t = MyThread()
        t.start()
        threads.append(t)
    for i in threads:
        i.join()

    print("end...")









