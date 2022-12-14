"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     GHDH_1_7.py
@Author:   shenfan
@Time:     2022/10/20 13:59

单体审查
"""
from Xboard.Delivery.deliveryCheck.GHDH import GHDH
from jsonpath import jsonpath


def ghdh_1_7():
    pad = GHDH(r"C:\Users\SHENFAN\Desktop\中设数字\CBIM-中设数字-CIM包\CIM\海口项目", "总图0927.cim")
    buildingList = pad.buildinglist()
    checkTables = {}
    buildingNo = jsonpath(buildingList, "$[?(@.buildingNo)].buildingNo")
    checkTables = dict(zip(tuple(buildingNo), {}))


ghdh_1_7()