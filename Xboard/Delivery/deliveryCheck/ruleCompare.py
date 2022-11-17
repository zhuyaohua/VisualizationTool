"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     ruleCompare.py
@Author:   shenfan
@Time:     2022/11/16 10:27

规则合法值匹配
"""
import re
from decimal import Decimal
import interval
from Xboard.Delivery.deliveryCheck.rule import rule
from Xboard.Delivery.deliveryCheck.CAD import componentList


def ruleCompare(ruleData, resultParam):
    for ruleitem in ruleData:
        func = lambda x: re.findall(r"\d+\.?\d*", x)
        for item in ruleitem:
            for key, value in item.items():
                if resultParam not in key:
                    values = value
                    if (value.startswith("(") or value.startswith("[")) and (
                            value.endswith(")") or value.endswith("]")):
                        if len(func(value)) == 1:
                            if value.find(",") > value.find(func(value)[0]) and value.startswith("["):
                                values = interval.Interval(Decimal(func(value)[0]), float("inf"), upper_closed=False)
                            if value.find(",") > value.find(func(value)[0]) and value.startswith("("):
                                values = interval.Interval(Decimal(func(value)[0]), float("inf"), lower_closed=False,
                                                           upper_closed=False)
                            if value.find(",") < value.find(func(value)[0]) and value.endswith("]"):
                                values = interval.Interval(Decimal(func(value)[0]), -float("inf"), lower_closed=False)
                            if value.find(",") < value.find(func(value)[0]) and value.endswith(")"):
                                values = interval.Interval(Decimal(func(value)[0]), -float("inf"), lower_closed=False,
                                                           upper_closed=False)
                            if value.find(",") < 0:
                                values = interval.Interval(Decimal(func(value)[0]), Decimal(func(value)[0]))
                        if len(func(value)) == 2:
                            if value.startswith("[") and value.endswith("]"):
                                values = interval.Interval(Decimal(func(value)[0]), Decimal(func(value)[1]),
                                                           lower_closed=True, upper_closed=True)
                            if value.startswith("(") and value.endswith("]"):
                                values = interval.Interval(Decimal(func(value)[0]), Decimal(func(value)[1]),
                                                           lower_closed=False, upper_closed=True)
                            if value.startswith("[") and value.endswith(")"):
                                values = interval.Interval(Decimal(func(value)[0]), Decimal(func(value)[1]),
                                                           lower_closed=True, upper_closed=False)
                            if value.startswith("(") and value.endswith(")"):
                                values = interval.Interval(Decimal(func(value)[0]), Decimal(func(value)[1]),
                                                           lower_closed=False, upper_closed=False)
                        if len(func(value)) == 0:
                            values = interval.Interval(-float("inf"), float("inf"), upper_closed=False,
                                                       lower_closed=False)
                        item[key] = values
    return ruleData


def check(rules, datas, resultParam):
    global legalKey
    print("\033[1;31m匹配中\033[0m", "\033[1;31m...\033[0m" * 10)
    rule = []
    for item_rule in rules:
        temp = {}
        for item in item_rule:
            temp.update(item)
        rule.append(temp)
    ruleKeys = list(rule[0].keys())
    for item in ruleKeys:
        if resultParam in item:
            legalKey = item
    for data in datas:
        flag = True
        print("*" * 50)
        legalValue = "\033[1;31mNO Match\033[0m"
        count = 0
        # 某一条原模型数据
        checkDatas = []
        # for dataKey, dataValue in data.items():
        #     print(dataKey)
        #     for ruleKey in ruleKeys:
        #         print(ruleKey)
        #         if dataKey in ruleKey:
        #             checkDatas.append((dataKey, ruleKey))
        #         else:
        #             if resultParam not in ruleKey:
        #                 missingDatas.append(ruleKey)
        #             flag = False
        for ruleKey in ruleKeys:
            for dataKey, dataValue in data.items():
                if dataKey in ruleKey and dataKey != "uids":
                    checkDatas.append((dataKey, ruleKey))
                    continue
        temp = [item_check[1] for item_check in checkDatas]
        missingDatas = list(set(ruleKeys) - set(temp))
        for item_miss in missingDatas:
            if resultParam in item_miss:
                missingDatas.remove(item_miss)
            else:
                flag = False
        if flag:
            for itemRule in rule:
                count += 1
                print("尝试%d次匹配中..." % count)
                for checkData in checkDatas:
                    print("\033[1;31m %s\033[0m匹配详情：【模型参数】\033[1;31m %s\033[0m => 【合法参数】\033[1;31m %s\033[0m"% (checkData[0],data[checkData[0]], itemRule[checkData[1]]))
                    # 匹配参数
                    try:
                        if itemRule[checkData[1]] == "ALL":
                            continue
                        else:
                            flag = data[checkData[0]] in itemRule[checkData[1]]
                            if not flag:
                                print("跳出参数匹配")
                                break
                    except Exception as e:
                        flag = data[checkData[0]] in itemRule[checkData[1]]
                        if not flag:
                            print("跳出参数匹配")
                            break
                    # if itemRule[checkData[1]] == "ALL":
                    #     continue
                    # else:
                    #     flag = data[checkData[0]] in itemRule[checkData[1]]
                    #     if not flag:
                    #         print("跳出参数匹配")
                    #         break
                if not flag: continue
                if flag:
                    legalValue = itemRule[legalKey]
                    print("\033[1;32m在第%d次命中\033[0m" % count)
                    break
            if count == len(rule):
                legalValue = "\033[1;31mNO Match（规则库无合法值,请检查规则库）\033[0m"
        else:
            print("\033[1;32m缺少的合法值参数")
            print(list(set(missingDatas)))
            print("\033[0m")
        data.update({legalKey: legalValue})
    return datas


if __name__ == "__main__":
    check(ruleCompare(rule("结构-项目结构信息-高宽比"), "SC-S-108"),
          componentList("大庆案例 - 1117.cim", "XMJGXX")["XMJGXX"], "SC-S-108")
    # ruleCompare(rule("结构-项目结构信息-高宽比"), "SC-S-108")
