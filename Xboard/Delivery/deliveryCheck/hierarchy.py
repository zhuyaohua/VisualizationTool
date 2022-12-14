"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     hierarchy.py
@Author:   shenfan
@Time:     2022/10/20 17:27

审查项数据（包含cda.json和pda.json）
"""
import json
from jsonpath import jsonpath
from DataTools.visual_table import table
from DataTools.mysql_action import mysqldb
from Xboard.Delivery.deliveryCheck.CAD import componentList
from Xboard.Delivery.deliveryCheck.ruleCompare import check, ruleCompare, rule
import os
import pandas

db = mysqldb(host="172.16.211.46", port=3306, user="cbim_rule_read", passwd="roWWy650", database="cbim_rule")


def config(rule_code, audit_model_name):
    cmd = """
        SELECT audit_model_name,param_code,param_name,is_check,is_linkage,linkage_way
        FROM audit_config_form
        WHERE hierarchy_id = (SELECT id FROM hierarchy_class_lib WHERE rule_code = "{0}") AND audit_model_name = "{1}"
        """.format(rule_code, audit_model_name)
    params = db.db_action(cmd)[["param_code", "param_name"]].values
    audit_model_data = {}
    for item in params:
        audit_model_data.setdefault("{0} {1}".format(item[0], item[1]), {"value": None, "uids": []})
    return audit_model_data


def hierarchyPDA(rule_code, audit_model_name, modelname):
    with open(os.path.join(
            os.path.join(os.path.abspath(".."), "unzipfiles", modelname[:-4], "checkdata", "%s.json" % modelname[:-4])),
            "r", encoding="UTF-8") as strem:
        data = json.loads(strem.read())
    checkTables = {}
    checkTableHeaders = config(rule_code, audit_model_name)
    dataframe = []

    if "GH-A-109 建筑编号" in checkTableHeaders:
        buildingdatas = jsonpath(data, "$..buildings")
        if buildingdatas:
            for buildingdata in buildingdatas:
                for item in buildingdata:
                    checkTables[item] = checkTableHeaders
                    temp = {}
                    for key in checkTableHeaders:
                        result = jsonpath(buildingdata, "$..%s" % key)[0] if jsonpath(buildingdata,
                                                                                      "$..%s" % key) else {"value": 0.0,
                                                                                                           "uids": []}
                        checkTableHeaders[key] = result
                        temp[key] = checkTableHeaders[key]["value"]
                    dataframe.append(temp)
    if "GH-A-207 贴线率" in checkTableHeaders:
        lineRateDatas = jsonpath(data, "$..nearLineRateList")
        for lineRateData in lineRateDatas:
            for item in lineRateData:
                temp = {}
                for key in checkTableHeaders:
                    result = jsonpath(item, "$..%s" % key)[0] if jsonpath(item, "$..%s" % key) else {"value": 0.0,
                                                                                                     "uids": []}
                    checkTableHeaders[key] = result
                    temp[key] = checkTableHeaders[key]["value"]
                dataframe.append(temp)
    else:
        for item in data:
            checkTables[item] = checkTableHeaders
            temp = {}
            for key in checkTableHeaders:
                checkTableHeaders[key] = jsonpath(data, "$.%s.%s" % (item, key))[0]
                temp[key] = checkTableHeaders[key]["value"]
            dataframe.append(temp)

    dataframe = pandas.DataFrame(dataframe, index=None)
    dataframe = dataframe.to_dict(orient="list")

    tableHeaders = list(dataframe.keys())
    tableValues = list(dataframe.values())
    table(tableHeaders, tableValues)


def hierarchyCDA(rule_code, audit_model_name, modelname, type, ruleName, resultParam):
    datas = componentList(modelname, type)
    checkTables = {}
    checkTableHeaders = config(rule_code, audit_model_name)
    dataframe = []

    datas = check(ruleCompare(rule(ruleName), resultParam), datas[type], resultParam)

    for item in datas:
        temp = {}
        for key in checkTableHeaders:
            if key.split(" ")[0] in item:
                temp[key] = item[key.split(" ")[0]]
            else:
                temp[key] = "模型中没有此参数"
        dataframe.append(temp)

    dataframe = pandas.DataFrame(dataframe, index=None)
    for item in datas:
        for key, value in item.items():
            if key != "uids":
                if resultParam in key:
                    print("\033[1;31m 构件的合法值为：\033[0m")
                print(key, "==>", value)
        print(item["uids"])
        print("*" * 50)
    dataframe = dataframe.to_dict(orient="list")

    tableHeaders = list(dataframe.keys())
    tableValues = list(dataframe.values())
    table(tableHeaders, tableValues)


if __name__ == "__main__":
    # hierarchyPDA("GH-DH-13", "地上退让审查（控规图则）", "总图贴现率.jdm")
    hierarchyCDA("JGSC-DH-A_A-1-1", "项目结构信息", "大庆案例 - 1117.cim", "XMJGXX", "结构-项目结构信息-高宽比", "SC-S-108")
    # config("GH-DH-13", "地上退让审查（控规图则）")
