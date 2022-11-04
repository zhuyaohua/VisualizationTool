"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     workingHours.py
@Author:   shenfan
@Time:     2022/11/3 14:29
"""
from DataTools.mysql_action import mysqldb
import os
import pandas

db = mysqldb(host="172.16.201.101", port=3306, user="test1", passwd="4&@LkQ7&4XbM", database="zentao")
dirpath = os.path.join(os.path.dirname(os.path.abspath(".")), "Data", "outputfile")


def taskDetails(dept):
    """
    任务工时详情
    :param dept: 部门名称
    :return: Excel
    """
    cmd_details = """
    SELECT
zt_product.`name` AS "所属产品",
zt_project.`name` AS "所属项目",
zt_task.`name` AS "任务",
zt_task.pri AS "优先级",
zt_task.estimate AS "预计工时",
zt_task.consumed AS "消耗工时",
zt_task.`left` AS "剩余工时",
zt_user.realname AS "责任人",
zt_task.deadline AS "任务截止时间",
zt_dept.`name` AS "部门"
FROM
	zt_task
LEFT JOIN zt_project ON zt_project.id = zt_task.project
LEFT JOIN zt_projectproduct ON zt_projectproduct.project = zt_task.project
LEFT JOIN zt_product ON zt_product.id = zt_projectproduct.product
LEFT JOIN zentao.zt_user ON zt_user.account = zt_task.assignedTo
LEFT JOIN zentao.zt_dept ON zt_dept.id = zt_user.dept
WHERE
	zt_task.deleted = 1 AND date_format(zt_task.openedDate,'%Y-%m')=date_format(now(),'%Y-%m') and zt_product.`name` = "八仙平台XBOAT" AND zt_dept.`name` = "{0}"
ORDER BY zt_user.realname,zt_project.`name`;
    """
    task_details = db.db_action(cmd_details.format(dept))
    cmd_summary = """
    SELECT
zt_product.`name` AS "所属产品",
zt_project.`name` AS "所属项目",
zt_user.realname AS "责任人",
SUM(zt_task.estimate) AS "预计总工时"
FROM
	zt_task
LEFT JOIN zt_project ON zt_project.id = zt_task.project
LEFT JOIN zt_projectproduct ON zt_projectproduct.project = zt_task.project
LEFT JOIN zt_product ON zt_product.id = zt_projectproduct.product
LEFT JOIN zentao.zt_user ON zt_user.account = zt_task.assignedTo
LEFT JOIN zentao.zt_dept ON zt_dept.id = zt_user.dept
WHERE
	zt_task.deleted = 1 AND date_format(zt_task.openedDate,'%Y-%m')=date_format(now(),'%Y-%m') and zt_product.`name` = "八仙平台XBOAT" AND zt_dept.`name` = "{0}"
GROUP BY zt_user.realname,zt_project.`name`
ORDER BY zt_user.realname,zt_project.`name`;
    """
    task_summary = db.db_action(cmd_summary.format(dept))

    writer = pandas.ExcelWriter(os.path.join(dirpath, "WorkHours.xls"))
    task_details.to_excel(writer, sheet_name="任务详情", index=None)
    task_summary.to_excel(writer, sheet_name="工时总计", index=None)
    writer.save()
    writer.close()


if __name__ == "__main__":
    taskDetails(" 平台测试")
