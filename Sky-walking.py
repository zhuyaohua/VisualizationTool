"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     Sky-walking.py
@Author:   shenfan
@Time:     2022/9/21 17:02
"""
import requests
import pandas
import datetime
import os

headers = {"Content-Type": "application/json;charset=UTF-8"}
url = "http://172.16.211.18:58080/graphql"

datas = []
for i in range(1, 11):
    data = {
        "query": "query queryTraces($condition: TraceQueryCondition) {\n  data: queryBasicTraces(condition: $condition) {\n    traces {\n      key: segmentId\n      endpointNames\n      duration\n      start\n      isError\n      traceIds\n    }\n    total\n  }}",
        "variables": {"condition": {"queryDuration": {"start": "2022-09-20 13", "end": "2022-09-20 20", "step": "HOUR"},
                                    "traceState": "ALL", "paging": {"pageNum": i, "pageSize": 1000, "needTotal": True},
                                    "queryOrder": "BY_DURATION"}}}
    result = requests.post(url=url, headers=headers, json=data, verify=False).json()

    for item in result["data"]["data"]["traces"]:
        datas.append(dict(zip(("开始时间", "接口", "耗时"), (
            datetime.datetime.fromtimestamp(int(item["start"]) / 1000).strftime("%y-%m-%d %H:%M:%S"), item["endpointNames"][0],
            item["duration"]))))

dataframe = pandas.DataFrame(datas, index=None)
output_dir = os.path.join(os.path.dirname(os.path.abspath("__file__")), "Data", "outputfile")

dataframe.to_excel(os.path.join(output_dir, "skywalking.xls"), sheet_name="skywalking", index=False)
