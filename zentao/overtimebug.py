"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     overtimebug.py
@Author:   shenfan
@Time:     2022/10/11 9:33
"""
from DataTools.mysql_action import mysqldb
from Data.data_output import savefile
import os
from lxml import etree
import html2text

db = mysqldb(host="172.16.201.101", port=3306, user="test1", passwd="4&@LkQ7&4XbM", database="zentao")
cmd = """
SELECT
  temp.id AS "Bug编号",
	temp.product AS "所属产品",
  IFNULL(temp.`name`,"-") AS "所属模块",
	temp.project AS "所属项目",
	temp.title AS "Bug标题",
	CASE
WHEN temp.severity = 1 THEN "A 致命"
WHEN temp.severity = 2 THEN "B 严重"
WHEN temp.severity = 3 THEN "C 一般"
WHEN temp.severity = 4 THEN "D 轻微"
WHEN temp.severity = 5 THEN "E 建议"
END AS "严重程度",
	CASE
WHEN temp.pri = 1 THEN "P0"
WHEN temp.pri = 2 THEN "P1"
WHEN temp.pri = 3 THEN "P2"
WHEN temp.pri = 4 THEN "P3"
WHEN temp.pri = 5 THEN "P4"
END AS "优先级",
CONCAT("http://zentao.cbim.org.cn/zentao/bug-view-",temp.id,".html") AS "重现步骤",
	CASE
WHEN temp.`status` = "active" THEN "激活"
WHEN temp.`status` = "resolved" THEN "已解决"
END as "Bug状态",
temp.creator AS "由谁创建",
temp.createtime AS "创建日期",
zt_user.realname AS "指派给",
temp.assignedtime AS "指派日期",
temp.activetime AS "超时天数",
"" AS "超时未修复原因",
"" AS "预计修改时间",
"" AS "备注"
FROM
	(
		SELECT
			zt_bug.id,
      zt_module.`name`,
			zt_product.`name` AS product,
			IFNULL(zt_project.`name`, "-") AS project,
			zt_bug.title,
			zt_bug.severity,
			zt_bug.pri,
			zt_bug.steps,
			zt_bug.`status`,
			zt_user.realname AS creator,
			zt_bug.assignedTo,
			datediff(
				date_format(now(), '%Y-%m-%d'),
				date_format(zt_bug.openedDate,'%Y-%m-%d')
			) AS activetime,
			date_format(
			  zt_bug.openedDate,'%Y-%m-%d'
			) AS createtime,
			date_format(
				zt_bug.assignedDate,'%Y-%m-%d'
			) AS assignedtime,
        zt_bug.deleted
		FROM
			zentao.zt_bug
		LEFT JOIN zentao.zt_user ON zt_user.account = zt_bug.openedBy
		LEFT JOIN zentao.zt_project ON zt_project.id = zt_bug.project
		LEFT JOIN zentao.zt_product ON zt_product.id = zt_bug.product
    LEFT JOIN zentao.zt_module ON zt_module.id = zt_bug.module
		WHERE
			zt_bug.`status` = "active"
		AND zt_product.`name` = "八仙平台XBOAT" AND zt_bug.deleted = "0" 
	) temp
LEFT JOIN zentao.zt_user ON zt_user.account = temp.assignedTo
WHERE temp.activetime >= 2 AND temp.project <> "XBOAT-线上问题"
"""

dirpath = os.path.join(os.path.dirname(os.path.abspath(".")), "Data", "outputfile")
dataframe = db.db_action(cmd)
savefile(dataframe, "超过两天未修改bug记录.xls", dirpath, filetype="xls")
