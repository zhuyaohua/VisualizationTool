"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     mysql_action.py
@Author:   shenfan
@Time:     2022/8/10 15:06
"""
import pymysql
import prettytable
import pandas
import re


class mysqldb:
    def __init__(self, host, port, user, passwd, database=None):
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, database=database)
        self.cur = self.conn.cursor()

    def db_action(self, cmd):
        if bool(re.search('select', cmd, re.IGNORECASE)):
            print("\033[1;34m*\033[0m" * 30)
            print("Execution SQL：")
            print(cmd)
            print("\033[1;34m*\033[0m" * 30)
            print("\033[1;34mResult:\033[0m")
            self.cur.execute(cmd)
            feilds = [item[0] for item in self.cur.description]
            table = prettytable.PrettyTable()
            table.field_names = feilds
            result_raw = self.cur.fetchall()
            result = pandas.DataFrame(result_raw, columns=feilds)
            result = result.where(result.notnull(), "-")

            for item in result.values:
                table.add_row(list(item))
            print(table)
            print("\033[1;34m#\033[0m" * 120)
            return result
        else:
            self.cur.execute(cmd)
            self.conn.commit()
