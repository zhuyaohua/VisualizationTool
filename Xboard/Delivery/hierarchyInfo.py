"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     hierarchyInfo.py
@Author:   shenfan
@Time:     2022/10/25 15:12
"""
import json
from jsonpath import jsonpath
from DataTools.visual_table import table
from DataTools.mysql_action import mysqldb
import os
import pandas

db = mysqldb(host="172.16.211.46", port=3306, user="cbim_rule_read", passwd="roWWy650", database="cbim_rule")


def hierarchyInfo():
    cmd = """SELECT rule_value.rule_code,rr.`审查项`,rr.type,rr.`专业`,rr.`城市`,rr.`规范条目数` FROM
(SELECT rule_value.rule_value AS "审查项",oo.rule_value AS "type",oo.`专业`,oo.`城市`,oo.`规范条目数`,hierarchy_class_lib.parent_line_num FROM 
(SELECT ll.rule_value,ll.`专业`,ll.`城市`,rule_value.rule_value AS "规范条目数",ll.line_num FROM
(SELECT nn.rule_value,nn.`专业`,rule_value.rule_value AS "城市",nn.line_num FROM
(SELECT mm.rule_value,rule_value.rule_value AS "专业",mm.line_num FROM 
(SELECT rule_value.rule_value,rule_value.line_num FROM rule_value 
LEFT JOIN rule_param ON rule_param.id = rule_value.head_id
WHERE rule_param.param_value_id = "41415" AND rule_value.rule_lib_id in (SELECT id FROM cbim_rule.rule_lib WHERE lib_code in ("GH-DH","ZNSC","SZGC-DH","ZYTZ","JSGL-DH-1","JGSC-DH") AND lib_status =0)
HAVING rule_value <> "") mm
LEFT JOIN rule_value ON rule_value.line_num = mm.line_num
LEFT JOIN rule_param ON rule_param.id = rule_value.head_id
WHERE rule_param.param_value_id = "18236") nn
LEFT JOIN rule_value ON rule_value.line_num = nn.line_num
LEFT JOIN rule_param ON rule_param.id = rule_value.head_id
WHERE rule_param.param_value_id = "43983") ll
LEFT JOIN rule_value ON rule_value.line_num = ll.line_num
LEFT JOIN rule_param ON rule_param.id = rule_value.head_id
WHERE rule_param.param_value_id = "52762") oo
LEFT JOIN rule_value ON rule_value.line_num = oo.line_num
LEFT JOIN hierarchy_class_lib on hierarchy_class_lib.line_num = oo.line_num
LEFT JOIN rule_param ON rule_param.id = rule_value.head_id
WHERE rule_param.param_value_id = "43973") rr
LEFT JOIN rule_value ON rule_value.line_num = rr.parent_line_num
LEFT JOIN rule_param ON rule_param.id = rule_value.head_id
WHERE rule_param.param_value_id = "46966"
    """
    datas = db.db_action(cmd)
    datas.to_excel("规则引擎数据-审查项.xls", index=None)
    print(datas)


if __name__ == "__main__":
    hierarchyInfo()


