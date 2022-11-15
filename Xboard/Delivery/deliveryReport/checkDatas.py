"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     checkDatas.py
@Author:   shenfan
@Time:     2022/11/14 14:11
"""
from DataTools.mysql_action import mysqldb

db = mysqldb(host="10.81.3.51", port=3306, user="cbim_delivery", passwd="cbim_delivery@Cbim2021", database="cbim_delivery")


def standardDetials(modelid):
    cmd = """
        SELECT 
            * 
        FROM
            (SELECT model_id,audit_page_code,audit_Item_name,standard,clauses,clauses_type 
                FROM rule_check 
                WHERE model_id =(SELECT source_id FROM doc_center WHERE doc_id="{0}") AND type = 3 
        UNION
            SELECT model_id,audit_page_code,audit_Item_name,standard,clauses,clauses_type 
                FROM manual_check WHERE model_id =(SELECT source_id FROM doc_center WHERE doc_id="{0}")
        ) m
    """
    checkDatas = db.db_action(cmd.format(modelid))
    return checkDatas


if __name__ == "__main__":
    standardDetials("893499353765208064")




