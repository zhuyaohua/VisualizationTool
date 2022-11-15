"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     taskInfo.py
@Author:   shenfan
@Time:     2022/11/14 11:12
"""
from DataTools.mysql_action import mysqldb

db = mysqldb(host="10.81.3.57",
             port=3306,
             user="cbim_task",
             passwd="cbim_task",
             database="cbim_task")


def taskInfo(objectid):
    cmd = """
        SELECT task_task.project_id,task_task.task_name 
        FROM task_scheme_file
        LEFT JOIN task_task ON task_task.id = task_scheme_file.task_task_id 
        WHERE task_scheme_file.file_id = "{0}"
    """
    taskModel = db.db_action(cmd.format(objectid))
    return taskModel


if __name__ == "__main__":
    taskInfo("893499353765208064")




