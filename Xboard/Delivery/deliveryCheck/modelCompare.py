"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     modelCompare.py
@Author:   shenfan
@Time:     2022/10/24 13:51
"""
import os
import fnmatch
import json
from jsonpath import jsonpath
import deepdiff

basePath = os.path.join(os.path.abspath(".."), "unzipfiles")


def modelDatas(Model):
    resultinfos = {"objects": [], "draws": None}
    targetPath = os.path.join(basePath, Model.split(".")[0])
    objects = []
    draws = []
    for root, dirs, files in os.walk(targetPath):
        for file in files:
            if fnmatch.fnmatch(file, '*.json'):
                mathFile = os.path.join(root, file)
                with open(mathFile, "r", encoding="UTF-8") as stream:
                    infos = json.loads(stream.read())
                    object = jsonpath(infos, "$.objects.components[?(@.uuid)]")
                    object = object if object else []
                    objects.extend(object)
            if file.split(".")[1] in ["dxf", "dwg"]:
                draws.append({"fileName": file, "fileCode": file[-18:-5]})
    for item in objects:
        temp = {item["uuid"] + "(%s)" % item["name"]: item["groupedUserData"]}
        resultinfos["objects"].append(temp)

    resultinfos["draws"] = draws
    return resultinfos


def compareModel(baseDatas: dict, referenceDatas: dict):

    objectdiff = deepdiff.DeepDiff(baseDatas["objects"], referenceDatas["objects"], view="tree", ignore_order=True)
    print("构件变更信息")
    for item in objectdiff:
        print(item)
        for i in objectdiff[item]:
            print(i)
    objectdiff = deepdiff.DeepDiff(baseDatas["draws"], referenceDatas["draws"], view="tree", ignore_order=True)
    print("图纸变更信息")
    for item in objectdiff:
        print(item)
        for i in objectdiff[item]:
            print(i)

    objectdiff = deepdiff.DeepDiff(baseDatas["draws"], referenceDatas["draws"], view="tree", ignore_order=True)
    print("图纸变更信息")
    for item in objectdiff:
        print(item)
        for i in objectdiff[item]:
            print(i)
    print("构件变更信息")


if __name__ == "__main__":
    r1 = modelDatas("万花项目0927.cim")
    r2 = modelDatas("万花项目0928.cim")
    compareModel(r1, r2)
