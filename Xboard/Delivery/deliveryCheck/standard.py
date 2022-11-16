"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     standard.py
@Author:   shenfan
@Time:     2022/11/3 16:07

导出所有的规范&具体规范详情
"""
from DataTools.mysql_action import mysqldb
import os
import pandas

db = mysqldb(host="172.16.211.46", port=3306, user="cbim_rule_read", passwd="roWWy650", database="cbim_rule")


def standard(standardName=None):
    cmd = """
    #人工审查规范
SELECT "人工审查" AS type,p.audit_model_name,m.standard_name,l.article_name,n.article_mandatory,k.article_content FROM
(SELECT rule_value.rule_lib_id,rule_value.rule_value AS standard_name,rule_value.line_num FROM cbim_rule.manual_audit_rule_relation
LEFT JOIN cbim_rule.rule_value ON rule_value.rule_lib_id = manual_audit_rule_relation.rule_lib_id
LEFT JOIN cbim_rule.rule_param ON rule_param.id = rule_value.head_id
WHERE rule_param.param_value_id ="-20002") m
LEFT JOIN 
(SELECT rule_value.rule_value AS article_mandatory,rule_value.line_num FROM cbim_rule.manual_audit_rule_relation
LEFT JOIN cbim_rule.rule_value ON rule_value.rule_lib_id = manual_audit_rule_relation.rule_lib_id
LEFT JOIN cbim_rule.rule_param ON rule_param.id = rule_value.head_id
WHERE rule_param.param_value_id ="-20004") n ON n.line_num = m.line_num
LEFT JOIN
(SELECT rule_value.rule_value AS article_name,rule_value.line_num FROM cbim_rule.manual_audit_rule_relation
LEFT JOIN cbim_rule.rule_value ON rule_value.rule_lib_id = manual_audit_rule_relation.rule_lib_id
LEFT JOIN cbim_rule.rule_param ON rule_param.id = rule_value.head_id
WHERE rule_param.param_value_id ="-20003") l ON l.line_num = m.line_num
LEFT JOIN 
(SELECT rule_value.rule_value AS article_content,rule_value.line_num FROM cbim_rule.manual_audit_rule_relation
LEFT JOIN cbim_rule.rule_value ON rule_value.rule_lib_id = manual_audit_rule_relation.rule_lib_id
LEFT JOIN cbim_rule.rule_param ON rule_param.id = rule_value.head_id
WHERE rule_param.param_value_id ="29869") k ON k.line_num = m.line_num
LEFT JOIN
(SELECT manual_audit_rule_relation.audit_model_name,manual_audit_rule_relation.rule_lib_name,manual_audit_rule_relation.rule_lib_id FROM hierarchy_class_lib
LEFT JOIN manual_audit_rule_relation ON manual_audit_rule_relation.hierarchy_id = hierarchy_class_lib.id
WHERE rule_code REGEXP "^(GH-DH|ZNSC|SZGC-DH|ZYTZ|JSGL-DH-1|JGSC-DH)" AND audit_page_type = 1
GROUP BY audit_model_name,rule_lib_name,rule_lib_id) p ON p.rule_lib_id = m.rule_lib_id
UNION ALL
#表单审查
SELECT "表单审查" AS type,temp.hierarchy_name AS "audit_model_name",temp.standard_name,temp.article_name,temp.article_mandatory,temp.article_content FROM(
SELECT hierarchy_class_lib.id,rule_lib.id AS rule_id,hierarchy_class_lib.hierarchy_name,audit_standard.id AS standardid,audit_standard.standard_name,audit_standard_detail.article_name,audit_standard_detail.article_content,audit_standard_detail.article_mandatory,rule_lib.lib_name FROM hierarchy_class_lib 
LEFT JOIN rule_lib ON rule_lib.id = hierarchy_class_lib.rule_lib_id
LEFT JOIN audit_standard ON audit_standard.hierarchy_id = hierarchy_class_lib.id
LEFT JOIN audit_standard_detail ON audit_standard_detail.audit_standard_id = audit_standard.id
WHERE 
rule_lib.lib_code in ("GH-DH","ZNSC","SZGC-DH","ZYTZ","JSGL-DH-1","JGSC-DH") AND rule_lib.lib_status =0 
HAVING audit_standard.id IS NOT NULL) temp
LEFT JOIN rule_value ON temp.hierarchy_name = rule_value.rule_value
AND rule_value.head_id = "1668";
    """

    cmd_filter = """
SELECT o.* FROM 
(#人工审查规范
SELECT "人工审查" AS type,p.audit_model_name,m.standard_name,l.article_name,n.article_mandatory,k.article_content FROM
(SELECT rule_value.rule_lib_id,rule_value.rule_value AS standard_name,rule_value.line_num FROM cbim_rule.manual_audit_rule_relation
LEFT JOIN cbim_rule.rule_value ON rule_value.rule_lib_id = manual_audit_rule_relation.rule_lib_id
LEFT JOIN cbim_rule.rule_param ON rule_param.id = rule_value.head_id
WHERE rule_param.param_value_id ="-20002") m
LEFT JOIN 
(SELECT rule_value.rule_value AS article_mandatory,rule_value.line_num FROM cbim_rule.manual_audit_rule_relation
LEFT JOIN cbim_rule.rule_value ON rule_value.rule_lib_id = manual_audit_rule_relation.rule_lib_id
LEFT JOIN cbim_rule.rule_param ON rule_param.id = rule_value.head_id
WHERE rule_param.param_value_id ="-20004") n ON n.line_num = m.line_num
LEFT JOIN
(SELECT rule_value.rule_value AS article_name,rule_value.line_num FROM cbim_rule.manual_audit_rule_relation
LEFT JOIN cbim_rule.rule_value ON rule_value.rule_lib_id = manual_audit_rule_relation.rule_lib_id
LEFT JOIN cbim_rule.rule_param ON rule_param.id = rule_value.head_id
WHERE rule_param.param_value_id ="-20003") l ON l.line_num = m.line_num
LEFT JOIN 
(SELECT rule_value.rule_value AS article_content,rule_value.line_num FROM cbim_rule.manual_audit_rule_relation
LEFT JOIN cbim_rule.rule_value ON rule_value.rule_lib_id = manual_audit_rule_relation.rule_lib_id
LEFT JOIN cbim_rule.rule_param ON rule_param.id = rule_value.head_id
WHERE rule_param.param_value_id ="29869") k ON k.line_num = m.line_num
LEFT JOIN
(SELECT manual_audit_rule_relation.audit_model_name,manual_audit_rule_relation.rule_lib_name,manual_audit_rule_relation.rule_lib_id FROM hierarchy_class_lib
LEFT JOIN manual_audit_rule_relation ON manual_audit_rule_relation.hierarchy_id = hierarchy_class_lib.id
WHERE rule_code REGEXP "^(GH-DH|ZNSC|SZGC-DH|ZYTZ|JSGL-DH-1|JGSC-DH)" AND audit_page_type = 1
GROUP BY audit_model_name,rule_lib_name,rule_lib_id) p ON p.rule_lib_id = m.rule_lib_id
UNION ALL
#表单审查
SELECT "表单审查" AS type,temp.hierarchy_name AS "audit_model_name",temp.standard_name,temp.article_name,temp.article_mandatory,temp.article_content FROM(
SELECT hierarchy_class_lib.id,rule_lib.id AS rule_id,hierarchy_class_lib.hierarchy_name,audit_standard.id AS standardid,audit_standard.standard_name,audit_standard_detail.article_name,audit_standard_detail.article_content,audit_standard_detail.article_mandatory,rule_lib.lib_name FROM hierarchy_class_lib 
LEFT JOIN rule_lib ON rule_lib.id = hierarchy_class_lib.rule_lib_id
LEFT JOIN audit_standard ON audit_standard.hierarchy_id = hierarchy_class_lib.id
LEFT JOIN audit_standard_detail ON audit_standard_detail.audit_standard_id = audit_standard.id
WHERE 
rule_lib.lib_code in ("GH-DH","ZNSC","SZGC-DH","ZYTZ","JSGL-DH-1","JGSC-DH") AND rule_lib.lib_status =0 
HAVING audit_standard.id IS NOT NULL) temp
LEFT JOIN rule_value ON temp.hierarchy_name = rule_value.rule_value
AND rule_value.head_id = "1668") o
WHERE o.standard_name = "{0}";
    """

    if standardName:
        result = db.db_action(cmd_filter.format(standardName))
    else:
        result = db.db_action(cmd)
        result.to_excel("全规范条文.xls", index=None)

    return result


if __name__ == "__main__":
    standard()



