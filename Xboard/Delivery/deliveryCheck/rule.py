"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     rule.py
@Author:   shenfan
@Time:     2022/11/15 18:15

规则库详情，根据规则库名查询
"""
import openpyxl
import pandas
from DataTools.mysql_action import mysqldb
import os

db = mysqldb(host="172.16.211.46", port=3306, user="cbim_rule_read", passwd="roWWy650", database="cbim_rule")


def rule(ruleName):
    cmd = """
        SELECT 
        param_value.param_value as param_code,
        temp.param_value,
        case temp.rule_value 
        WHEN "" THEN "ALL" ELSE temp.rule_value END AS rule_value,temp.line_num 
        FROM
        (SELECT param_value.param_value,rule_value.rule_value,rule_value.line_num,param_value.line_num as param_line_num FROM rule_lib
        LEFT JOIN rule_value ON rule_value.rule_lib_id = rule_lib.id
        LEFT JOIN rule_param ON rule_param.id = rule_value.head_id
        LEFT JOIN param_value ON param_value.id = rule_param.param_value_id
        WHERE rule_lib.lib_name = "{0}" AND (rule_value.head_type=0 or rule_value.head_type=1) AND param_value IS NOT NULL
        ORDER BY rule_value.line_num ASC,rule_value.head_id ASC) temp
        LEFT JOIN param_value ON param_value.line_num = temp.param_line_num
        WHERE param_value.param_head = "参数编号"
    """

    result = db.db_action(cmd.format(ruleName))

    temp = result.to_dict(orient="split")["data"]
    datas = {}
    for item in temp:
        datas.setdefault(item[3], [])
        datas[item[3]].append({"%s(%s)" % (item[1], item[0]): item[2]})

    rules = list(datas.values())
    datas = []
    for item in rules:
        temp = {}
        for value in item:
            temp.update(value)
        datas.append(temp)

    writer = pandas.ExcelWriter(os.path.join(os.path.abspath(".."), "datas", "规则引擎（合法值）.xlsx"), engine="openpyxl")
    book = openpyxl.load_workbook(writer.path)
    writer.book = book
    if ruleName not in book.sheetnames:
        print("\033[1;35m<<<<<规则引擎：%s 已保存至%s>>>>>>\033[0m" % (ruleName, writer.path))
        pandas.DataFrame(datas).to_excel(excel_writer=writer, sheet_name=ruleName, index=None)
    writer.save()
    writer.close()

    return rules



