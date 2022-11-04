"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     CAD.py
@Author:   shenfan
@Time:     2022/10/25 16:03
"""
from jsonpath import jsonpath
import os
import json


def componentList(modelName, type):
    baseDir = os.path.dirname(os.path.abspath("__file__"))
    fileDir = os.path.join(baseDir, "unzipfiles", modelName[:-4], "cda.json")
    with open(fileDir, "r", encoding="utf-8") as data:
        datas = json.load(data)
    components = jsonpath(datas, "$.objects..type")
    for item in components:
        if item == "GraphicLinkage":
            components.remove(item)

    componentDatas = jsonpath(datas, "$.objects[?(@.type=='%s')]" % type)
    GraphicLinkage = jsonpath(datas, "$.objects[?(@.type=='GraphicLinkage')]")
    uids = {}
    for item in GraphicLinkage:
        temp = {item["uid"]: item["properties"]}
        uids.update(temp)
    result = {type: []}
    for componentData in componentDatas:
        temp = {}
        temp.setdefault("uids", "模型中无对应联动信息")
        if componentData["uid"] in uids:
            temp = {"uids": uids[componentData["uid"]]}
        for item, value in componentData["properties"].items():
            temp[item] = value["Value"]
        result[type].append(temp)
    return result


if __name__ == "__main__":
    componentList("大庆案例 - 2020.jdm", "Rho_Beam")
