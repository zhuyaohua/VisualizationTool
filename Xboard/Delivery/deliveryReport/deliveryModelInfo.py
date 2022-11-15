"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     deliveryModelInfo.py
@Author:   shenfan
@Time:     2022/11/14 10:13
"""
from DataTools.mysql_action import mysqldb

db = mysqldb(host="10.81.3.51", port=3306, user="cbim_delivery", passwd="cbim_delivery@Cbim2021", database="cbim_delivery")


def modelInfo(objectId):
    cmd = """
        SELECT 
        doc_center.source_id AS model_id,
        doc_center.doc_id AS modelId,
        base_model.model_name,
        base_model.project_id,
        CASE 
        WHEN doc_center.source_type = 1 THEN "模型"
        WHEN doc_center.source_type = 2 THEN "图纸"
        WHEN doc_center.source_type = 3 THEN "文档"
        END AS "类型",
        CASE
        WHEN model_status.`status` = 1 THEN "待审查"
        WHEN model_status.`status` = 2 THEN "审查中"
        WHEN model_status.`status` = 3 THEN "已发布"
        END AS "审查状态"
        FROM cbim_delivery.doc_center
        LEFT JOIN cbim_delivery.base_model ON base_model.id = doc_center.source_id
        LEFT JOIN cbim_delivery.model_status ON model_status.model_id = doc_center.source_id
        WHERE doc_center.doc_id = "{0}"
    """
    deliveryModel = db.db_action(cmd.format(objectId))
    return deliveryModel


if __name__ == "__main__":
    modelInfo("893499353765208064")



