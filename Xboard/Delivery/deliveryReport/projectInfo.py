"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     projectInfo.py
@Author:   shenfan
@Time:     2022/11/14 10:54
"""
from DataTools.mysql_action import mysqldb

db = mysqldb(host="10.81.3.57",
             port=3306,
             user="project_approval_manage",
             passwd="project_approval_manage",
             database="project_approval_manage")


def modelProject(projectid):
    cmd = """SELECT master_id as "project_id",proj_name,proj_region FROM pro_approval WHERE master_id = "{0}"
    """
    projectModel = db.db_action(cmd.format(projectid))
    temp = []
    for item in projectModel["proj_region"].tolist():
        city = ""
        for value in eval(item):
            city = city + value["name"] + "&"
        temp.append(city.rstrip("&"))
    projectModel["proj_region"] = temp
    return projectModel


if __name__ == "__main__":
    modelProject("891756504246358016")
