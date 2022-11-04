"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     testsuit.py
@Author:   shenfan
@Time:     2022/9/20 9:31
"""
from DataTools.mysql_action import mysqldb
import altair as alt
import altair_viewer
import pandas

cmd = """
SELECT
zt_project.`name` AS project,
zt_product.`name` AS product,
zt_testtask.`name` AS testtask,
zt_testtask.`owner`,
date_format(zt_testtask.`begin`,'%Y-%m-%d'),
date_format(zt_testtask.`end`,'%Y-%m-%d'),
IFNULL(zt_testresult.caseResult,"unexecuted") caseResult
FROM
	zt_testrun
LEFT JOIN zt_testtask ON zt_testrun.task = zt_testtask.id
LEFT JOIN zt_project ON zt_project.id = zt_testtask.project
LEFT JOIN zt_product ON zt_product.id = zt_testtask.product
LEFT JOIN zt_testresult ON zt_testresult.`case` = zt_testrun.`case`
WHERE date_format(zt_testtask.`begin`,'%Y-%m')=date_format(now(),'%Y-%m') AND zt_testtask.deleted = "0";
"""
db = mysqldb(host="172.16.201.101", port=3306, user="test1", passwd="4&@LkQ7&4XbM", database="zentao")


def testsuit():
    source = db.db_action(cmd)

    bar = alt.Chart(source).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3
    ).encode(
        x='testtask:O',
        y='count():Q',
        color='caseResult:N'
    )
    altair_viewer.show(bar)


testsuit()

