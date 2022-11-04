"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     story.py
@Author:   shenfan
@Time:     2022/8/15 17:58
"""
from DataTools.mysql_action import mysqldb

db = mysqldb(host="172.16.201.101", port=3306, user="test1", passwd="4&@LkQ7&4XbM")
cmd = """
SELECT o.product,o.project,o.testtask,o.`owner`,o.`begin`,o.`end`,IFNULL(p.casenum,"-") as casenums,IFNULL(r.Pass,"-") as pass,IFNULL(r.Fail,"-") as fail,IFNULL(r.Bloack,"-") as bloack FROM 
(SELECT
zt_testtask.id,
zt_project.`name` AS project,
zt_product.`name` AS product,
zt_testtask.`name` AS testtask,
zt_testtask.`owner`,
zt_testtask.`begin`,
zt_testtask.`end`
FROM
	zentao.zt_testtask
LEFT JOIN zentao.zt_project ON zt_project.id = zt_testtask.project
LEFT JOIN zentao.zt_product ON zt_product.id = zt_testtask.product
WHERE date_format(zt_testtask.`begin`,'%Y-%m')=date_format(now(),'%Y-%m') AND zt_testtask.deleted = "0") o
LEFT JOIN 
(SELECT m.id AS testtask,COUNT(m.`case`) AS casenum FROM
(SELECT
zt_testtask.id,
zt_project.`name` AS project,
zt_product.`name` AS product,
zt_testtask.`name` AS testtask,
zt_testtask.`owner`,
zt_testtask.`begin`,
zt_testtask.`end`,
zt_testrun.`case`,
zt_testresult.caseResult
FROM
	zentao.zt_testtask
LEFT JOIN zentao.zt_project ON zt_project.id = zt_testtask.project
LEFT JOIN zentao.zt_product ON zt_product.id = zt_testtask.product
LEFT JOIN zentao.zt_testrun ON zt_testrun.task = zt_testtask.id
LEFT JOIN zentao.zt_testresult ON zt_testresult.run = zt_testrun.id
WHERE date_format(zt_testtask.`begin`,'%Y-%m')=date_format(now(),'%Y-%m') AND zt_testtask.deleted = "0") m
GROUP BY m.id) p ON p.testtask = o.id
LEFT JOIN (
SELECT n.id testtask,sum(n.Fail) Fail,sum(n.Pass) Pass ,sum(n.Bloack) Bloack FROM
(SELECT 
m.id,
CASE WHEN m.caseResult = "fail" THEN COUNT(m.caseResult) END AS Fail,
CASE WHEN m.caseResult = "pass" THEN COUNT(m.caseResult) END AS Pass,
CASE WHEN m.caseResult = "blocked" THEN COUNT(m.caseResult) END AS Bloack
FROM
(SELECT
zt_testtask.id,
zt_project.`name` AS project,
zt_product.`name` AS product,
zt_testtask.`name` AS testtask,
zt_testtask.`owner`,
zt_testtask.`begin`,
zt_testtask.`end`,
zt_testrun.`case`,
zt_testresult.caseResult
FROM
	zentao.zt_testtask
LEFT JOIN zentao.zt_project ON zt_project.id = zt_testtask.project
LEFT JOIN zentao.zt_product ON zt_product.id = zt_testtask.product
LEFT JOIN zentao.zt_testrun ON zt_testrun.task = zt_testtask.id
LEFT JOIN zentao.zt_testresult ON zt_testresult.run = zt_testrun.id
WHERE date_format(zt_testtask.`begin`,'%Y-%m')=date_format(now(),'%Y-%m') AND zt_testtask.deleted = "0") m
GROUP BY m.id,m.caseResult) n
GROUP BY n.id) r ON r.testtask = o.id
"""


def story_graphics(modelname):
    cmd.format(modelname)
    db.db_action(cmd)


story_graphics("BIM设计工具用户行为分析")
