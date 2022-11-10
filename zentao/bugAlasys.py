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
import pandas
import altair as alt
import altair_viewer

db = mysqldb(host="172.16.201.101", port=3306, user="test1", passwd="4&@LkQ7&4XbM", database="zentao")
cmd = """
SELECT 
zt_product.`name` AS product,
zt_project.`name` AS project,
m.story,
zt_module.`name` AS module,
zt_bug.title AS bug,
zt_bug.pri,
m.`需求截止时间`,
m.`需求实际提测时间`,
zt_bug.openedDate,
zt_bug.activatedCount
FROM
zentao.zt_bug
LEFT JOIN
(SELECT
zt_story.id,
zt_story.title AS story,
zt_story.openedDate,
MAX(zt_task.deadline) AS "需求截止时间",
MAX(zt_task.finishedDate) AS "需求实际提测时间"
FROM zentao.zt_story
LEFT JOIN zentao.zt_task ON zt_task.story = zt_story.id
GROUP BY zt_task.id) m ON m.id = zt_bug.toStory
LEFT JOIN zentao.zt_project ON zt_project.id = zt_bug.project
LEFT JOIN zentao.zt_product ON zt_product.id = zt_bug.product
LEFT JOIN zentao.zt_module ON zt_module.id = zt_bug.module
WHERE date_format(zt_bug.openedDate,"%Y-%m") = "{}" AND zt_product.`name` = "八仙平台XBOAT" and zt_bug.openedBy = "hejj"
"""

dirpath = os.path.join(os.path.dirname(os.path.abspath(".")), "Data", "outputfile")
dataframe = db.db_action(cmd.format("2022-10"))
savefile(dataframe, "bug分析.xls", dirpath, filetype="xls")

source = dataframe["openedDate"].tolist()
source = [str(item).split(" ")[0] for item in source]
data = {"category": [], "value": []}
for item in source:
    if item not in data["category"]:
        data["category"].append(item)
        data["value"].append(source.count(item))
data = pandas.DataFrame(data)
base = alt.Chart(data).encode(
    theta=alt.Theta("value:Q", stack=True),
    color=alt.Color("category:N", legend=None),
).properties(width=800, height=800)

pie = base.mark_arc(outerRadius=300)
text = base.mark_text(radius=360, size=10, angle=30).encode(text="category:N")
text1 = base.mark_text(radius=390, size=10, angle=30).encode(text="value:Q")

altair_viewer.show(pie + text + text1)


