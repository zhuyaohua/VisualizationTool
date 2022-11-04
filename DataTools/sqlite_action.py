"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     sqlite_action.py
@Author:   shenfan
@Time:     2022/8/8 17:45
"""
import sqlite3
import os
import re


class sqlitedb:
    def __init__(self, dbname, dbpasswd=None):
        self.dbname = dbname
        self.dbpasswd = dbpasswd
        self.conn = sqlite3.connect(self.dbname)
        self.cour = self.conn.cursor()
        if self.dbpasswd: self.cour.execute("PRAGMA KEY = '%s'" % self.dbpasswd)

    def db_action(self, cmd):
        if bool(re.search('select', cmd, re.IGNORECASE)):
            self.cour.execute(cmd)
            result = self.cour.fetchall()
            print(result)
            return result
        else:
            self.cour.execute(cmd)
            self.conn.commit()

    def db_close(self):
        self.cour.close()
        self.conn.close()


if __name__ == "__main__":
    file = r"C:\Users\SHENFAN\AppData\Roaming\CbimRevit\TempStatus.db"
    db = sqlitedb(os.path.abspath(file), dbpasswd="TempStatus123")
    cmd = "select * from sqlite_master where type='table' order by name"
    db.db_action(cmd)

