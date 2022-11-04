"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     json_extractor.py
@Author:   shenfan
@Time:     2022/8/11 15:26
"""
import jsonpath
import os
import json


def extractor(data, express, *args):
    result = jsonpath.jsonpath(data, express)
    data = []
    for item in result:
        data.append(dict(zip(args, tuple([item[i] for i in args]))))
    return data


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.path.abspath(".")), "Data", "Data.json"), "r", encoding="utf-8") as file:
        datas = json.loads(file.read())
    extractor(datas, "$.result..*[?(@.code != None)]", "code", "ruleLibCode")
