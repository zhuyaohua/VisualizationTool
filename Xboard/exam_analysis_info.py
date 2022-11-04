"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     exam_analysis_info.py
@Author:   shenfan
@Time:     2022/9/5 9:21
"""
from DataTools.mysql_action import mysqldb

db = mysqldb(host="10.80.252.199", port=3366, user="root", passwd="Cbim2021-")


def getUser(userid):
    cmd = """
    SELECT cbim_user.username FROM bms_bms.cbim_user
    WHERE  cbim_user.id= "{0}"
    """.format(userid)
    result = db.db_action(cmd)
    return result



