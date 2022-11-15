"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     dmsInfo.py
@Author:   shenfan
@Time:     2022/11/14 10:29
"""
from DataTools.mysql_action import mysqldb

db = mysqldb(host="10.80.252.199", port=3366, user="root", passwd="Cbim2021-")


def modelDms(objectid):
    cmd = """
        SELECT 
        cbim_enterprise.`name`,
        dms_bucket.app_code,
        dms_object.id AS modelId,
        dms_object.pathname,
        dms_object_tag.tag_value AS major 
        FROM dms_dms.dms_object
        LEFT JOIN dms_dms.dms_object_tag ON dms_object_tag.object_id = dms_object.id
        LEFT JOIN dms_dms.dms_bucket ON dms_bucket.id = dms_object.bucket_id
        LEFT JOIN bms_bms.cbim_enterprise ON cbim_enterprise.account_id = dms_bucket.account_id
        WHERE dms_object.id = "{0}" AND dms_object_tag.tag_key = "majorName";
    """
    dmsModle = db.db_action(cmd.format(objectid))
    return dmsModle


if __name__ == "__main__":
    modelDms("898202574052089856")



