"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     exam_analysis_datas.py
@Author:   shenfan
@Time:     2022/8/31 17:02
"""
from DataTools.mysql_action import mysqldb
import pandas
from Data.data_output import savefile

# db = mysqldb(host="10.81.3.57", port=3306, user="exam_analysis", passwd="exam_analysis@Cbim123")
# userdb = mysqldb(host="10.80.252.199", port=3366, user="root", passwd="Cbim2021-")
db = mysqldb(host="172.16.211.252", port=3366, user="exam_analysis_read", passwd="AykKM9ElPtoT")
userdb = mysqldb(host="172.16.211.251", port=3366, user="cbim", passwd="ChRd5@Hdhxt")

cmd = """
SELECT model_id,user_id,device_id,component_count,operation_type,component_add_count,operation_time 
FROM exam_analysis.operation_action 
WHERE user_id = "{0}" AND model_id= "{1}" 
ORDER BY operation_time ASC;
"""


def examAnalysisDatas(modelid, userid):
    raw = db.db_action(cmd.format(userid, modelid))
    # 构件总数
    compentTotalcount = int(raw[raw["operation_time"] == raw["operation_time"].max()]["component_count"])
    # 非原创构件数
    nonoriginal = raw[raw["operation_type"] == "增加"]["component_add_count"].sum(axis=0)
    # 原创构件数
    original = compentTotalcount - nonoriginal
    # 登录设备数
    devicenum = len(set(raw["device_id"]))
    # 起始构件数
    try:
        startCompent = raw["component_count"][0]
    except Exception as e:
        startCompent = 0
    # 未登录操作
    undatas = raw.sort_values(by="operation_time")[
        (raw["operation_type"] == "打开") | (raw["operation_type"] == "保存")].to_dict(orient="list")
    uncounts = 0
    uncompents = 0
    operationtype = undatas["operation_type"][undatas["operation_type"].index("保存"):]
    compents = undatas["component_count"][undatas["operation_type"].index("保存"):]
    temp = operationtype[1:]
    flag = 0
    for i in range(0, len(temp)):
        current = temp.pop(0)
        if current == "打开":
            uncompents += (compents[i + 1] - compents[flag])
            if uncompents > 0: uncounts += 1
        else:
            flag = i + 1
    data = {
        "构件总数": compentTotalcount,
        "原创构件数": original,
        "非原创构件数": nonoriginal,
        "原创构件比例": "%.2f%%" % (round(original / compentTotalcount, 4) * 100),
        "登录设备数": devicenum,
        "未登录操作次数": uncounts,
        "未登录操作构件": uncompents,
        "起始构件数": startCompent,
        "设备异常分布": raw[["device_id", "operation_time"]].to_dict(orient="records")
    }
    print(data)
    return data


cmddetail = """
SELECT model_id,user_id,operation_time
FROM exam_analysis.operation_action 
WHERE model_id= "{0}" 
ORDER BY operation_time ASC
"""
cmduser = """
    SELECT true_name,user_id FROM bms_bms.cbim_ent_user
    WHERE  user_id in {0} and ent_id = {1}
    """


def examAnalysisAcount(modelid,entid):
    raw = db.db_action(cmddetail.format(modelid))
    user = userdb.db_action(cmduser.format(tuple(raw["user_id"]),entid))
    result = pandas.merge(raw[["user_id", "operation_time"]].astype(str), user.astype(str), on="user_id", how="left")
    return result


cmdcounts = """
SELECT model_id,count(DISTINCT user_id) as acountcounts
FROM exam_analysis.operation_action 
WHERE model_id in {0}
GROUP BY model_id;
"""

userinfos = """
SELECT m.fileid,cbim_ent_user.true_name,m.file_tag as model_id FROM
(SELECT dms_bucket.app_code,dms_object.id AS fileid,dms_object.`name` AS filename,dms_object.pathname AS filepath,dms_object.created_by_id,dms_object.last_modified_by_id,dms_object.latest_version,dms_object_tag.tag_key AS file_tag_key,dms_object_tag.tag_value AS file_tag FROM dms_dms.dms_object
LEFT JOIN dms_dms.dms_object_tag ON dms_object_tag.object_id = dms_object.id
LEFT JOIN dms_dms.dms_bucket ON dms_bucket.id = dms_object.bucket_id
WHERE dms_object.id in {0} AND dms_object_tag.tag_key = "modelIds") m
LEFT JOIN bms_bms.cbim_ent_user ON bms_bms.cbim_ent_user.user_id = m.last_modified_by_id
WHERE cbim_ent_user.ent_id = {1}
"""


def examAnalysisAcounts(modelid: tuple, entid: str):
    users = userdb.db_action(userinfos.format(modelid, entid))
    raw = db.db_action(cmdcounts.format(tuple(users["model_id"].tolist())))
    result = pandas.merge(users, raw, on="model_id", how="left")
    result["user"] = result["true_name"] + " - " + result["fileid"].map(str)
    print(result)
    return result


if __name__ == "__main__":
    # examAnalysisAcount("8a06da6f-1ca1-42f8-b8cd-b7292902ddd6", "878941069851627520")
    # examAnalysisDatas("0f8088fb-e5b1-4fc9-b2b0-5aa245c3838f-9G-0913", "861664065313968128")
    import os
    dirpath = os.path.join(os.path.dirname(os.path.abspath(".")), "Data", "outputfile")
    db = mysqldb(host="172.16.211.252", port=3366, user="exam_analysis_read", passwd="AykKM9ElPtoT")
    cmd = """
    SELECT COUNT(0) FROM exam_analysis.operation_action WHERE model_id = "b193ea04-2161-44a5-b633-ce913af25215-CF" GROUP BY model_id
    """
    r = db.db_action(cmd)
    savefile(r, "bimT.xls", dirpath, filetype="xls")





