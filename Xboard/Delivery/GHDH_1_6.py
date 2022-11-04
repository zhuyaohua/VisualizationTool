"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     GHDH_1_6.py
@Author:   shenfan
@Time:     2022/10/18 9:11
"""
from jsonpath import jsonpath
from DataTools.visual_table import table
import json
import os


def ghdh_1_6(modelname, visual=False):

    with open(os.path.join(os.path.join(os.path.abspath("."), "unzipfiles", modelname[:-4], "checkdata","%s.json" % modelname[:-4])), "r", encoding="UTF-8") as strem:
        data = json.loads(strem.read())
    checkTables = {}
    for item in data:
        checkTableHeaders = {"GH-A-301 总用地面积": {"value": 0.0, "uids": []},
                             "GH-A-308 总建筑面积": {"value": 0.0, "uids": []},
                             "GH-A-87 地上计容面积": {"value": 0.0, "uids": []},
                             "GH-A-88 地上不计容面积": {"value": 0.0, "uids": []},
                             "GH-A-309 地下建筑总面积": {"value": 0.0, "uids": []},
                             "GH-A-403 地块计容总建筑面积": {"value": 0.0, "uids": []},
                             "GH-A-89 建筑基底总面积": {"value": 0.0, "uids": []},
                             "GH-A-90 道路广场面积": {"value": 0.0, "uids": []},
                             "GH-A-473 绿地面积": {"value": 0.0, "uids": []},
                             "GH-A-312 容积率": {"value": 0.0, "uids": []},
                             "GH-A-317 建筑密度": {"value": 0.0, "uids": []},
                             "GH-A-313 绿地率": {"value": 0.0, "uids": []},
                             "GH-A-182 建筑高度（m）": {"value": 0.0, "uids": []},
                             "GH-A-29 地上机动车位数": {"value": 0.0, "uids": []},
                             "GH-A-32 地下机动车位数": {"value": 0.0, "uids": []},
                             "GH-A-143 机动车位数": {"value": 0.0, "uids": []},
                             "GH-A-358 无障碍车位数": {"value": 0.0, "uids": []},
                             "GH-A-368 充电桩车位数量": {"value": 0.0, "uids": []},
                             "GH-A-91 地上非机动车位数": {"value": 0.0, "uids": []},
                             "GH-A-92 地下非机动车位数": {"value": 0.0, "uids": []},
                             "GH-A-367 非机动车位数": {"value": 0.0, "uids": []}
                             }
        checkTables[item] = checkTableHeaders
        for key in checkTableHeaders:
            checkTableHeaders[key] = jsonpath(data, "$.%s.%s" % (item, key))[0]

        if visual:
            tableheaders = ["主要技术经济指标表(地块：%s)" % (item), "数值"]
            tablevalues = [list(checkTableHeaders.keys())]
            temp = []
            for key in checkTableHeaders:
                temp.append(checkTableHeaders[key]["value"])
            tablevalues.append(temp)
            table(tableheaders, tablevalues)

    return checkTables


if __name__ == "__main__":
    ghdh_1_6("总图0927.cim", visual=True)
