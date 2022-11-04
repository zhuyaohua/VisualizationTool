"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     thread-07.py
@Author:   shenfan
@Time:     2022/9/29 14:32
"""
import threading,time


class SysThread(threading.Thread):
    def run(self) -> None:
        if semaphore.acquire():
            print(self.name, self.is_alive(),time.ctime())
            time.sleep(1)
            semaphore.release()
            print("*"*20)
            time.sleep(1)




if __name__ == "__main__":
    semaphore = threading.Semaphore(3)
    thds = []
    for i in range(10):
        t = SysThread()
        thds.append(t)
    for thd in thds:
        thd.start()
    for thd in thds:
        thd.join()

    print("end...")
