"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     bug.py
@Author:   shenfan
@Time:     2022/9/16 14:17
"""
from DataTools.mysql_action import mysqldb
import altair as alt
import altair_viewer
import threading
from functools import wraps

db = mysqldb(host="172.16.201.101", port=3306, user="test1", passwd="4&@LkQ7&4XbM")

cmd = """
SELECT zt_product.`name` AS product,IFNULL(zt_project.`name`,"non-project") AS project,COUNT(0) AS bugnum,zt_user.realname,zt_bug.pri,zt_bug.`status`,date_format(zt_bug.openedDate,'%Y-%m-%d') AS openedDate,date_format(zt_bug.closedDate,'%Y-%m-%d') AS closedDate FROM zentao.zt_bug
LEFT JOIN zentao.zt_user ON zt_user.account = zt_bug.openedBy
LEFT JOIN zentao.zt_project ON zt_project.id = zt_bug.project
LEFT JOIN zentao.zt_product ON zt_product.id = zt_bug.product
WHERE date_format(zt_bug.openedDate,'%Y-%m')=date_format(now(),'%Y-%m') 
GROUP BY zt_project.`name`,zt_user.realname,zt_bug.`status`
"""

source = db.db_action(cmd)


def addfillter(func):
    @wraps(func)
    def wrapper(condition: dict):
        data = source[source[condition["key"]] == condition["value"]]
        func(data)
        return func

    return wrapper


@addfillter
def bug_user_graphics(data):
    domain = ['closed', 'active', 'resolved']
    range_ = ['green', 'red', 'blue']
    bars = alt.Chart(data).mark_bar().encode(
        x=alt.X('sum(bugnum):Q', stack='zero', title="BUG总数"),
        y=alt.Y('realname:N', sort=[]),
        color=alt.Color('status', scale=alt.Scale(domain=domain, range=range_))
    )
    text = alt.Chart(data).mark_text(dx=-15, dy=2, color='white').encode(
        x=alt.X('sum(bugnum):Q', stack='zero'),
        y=alt.Y('realname:N', title="人员"),
        detail='status:N',
        text=alt.Text('sum(bugnum):Q')
    )
    s = (bars + text).interactive().properties(width=1200, height=900)
    altair_viewer.show(s)


def bug_project_graphics():
    chart = alt.Chart(source)
    bar = chart.mark_bar().encode(
        y=alt.Y('sum(bugnum):Q', stack='zero', title="总数"),
        x=alt.X('project:N', title="项目", axis={"labelAngle": 15}),
        color=alt.Color('status')
    )
    text = chart.mark_text(dx=0, dy=0, color='white').encode(
        x=alt.X('project:N', stack='zero'),
        y=alt.Y('sum(bugnum):N'),
        text=alt.Text('sum(bugnum):Q')
    )

    s = (bar + text).interactive().properties(width=1200, height=600)
    altair_viewer.show(s)


def bug_graphics(product="八仙平台XBOAT", type="active"):
    temp_source = source[(source["status"] == type) & (source["product"] == product)]

    line = alt.Chart(temp_source).mark_line(color="green").encode(
        x=alt.X(
            field='openedDate',
            type='temporal',
            sort='ascending',
            timeUnit="yearmonthdate",
            axis={"labelAngle": 15},
            title="时间"
        ),
        y=alt.Y("sum(bugnum):Q", title="总数")
    )
    altair_viewer.show(line.interactive().properties(width=1200, height=600))


# bug_user_graphics.__wrapped__(source)
bug_user_graphics({"key": "product", "value": "八仙平台XBOAT"})
