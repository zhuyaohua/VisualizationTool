"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     presonalWorkHours.py
@Author:   shenfan
@Time:     2022/11/10 17:00
"""
from DataTools.mysql_action import mysqldb
import datedays
from datetime import datetime
import altair as alt
import altair_viewer

db = mysqldb(host="172.16.201.101", port=3306, user="test1", passwd="4&@LkQ7&4XbM", database="zentao")


def personalWorkHours(dept, name, date):
    cmd = """
    SELECT zt_user.realname,ROUND(SUM(zt_effort.consumed),1) AS "Total",date_format(zt_effort.date,'%Y-%m-%d') AS "date" FROM zentao.zt_effort
LEFT JOIN zentao.zt_user ON zt_user.account = zt_effort.account
LEFT JOIN zentao.zt_dept ON zt_dept.id = zt_user.dept
WHERE zt_dept.`name` = "{dept}" AND zt_effort.deleted = 1 AND date_format(zt_effort.date,'%Y-%m') = "{date}" AND zt_user.realname = "{name}"
GROUP BY zt_user.realname,date_format(zt_effort.date,'%Y-%m-%d');
    """
    source = db.db_action(cmd.format(dept=dept, name=name, date=date))

    dates = datedays.gettodaydays(date+"-1")
    for item in dates:
        if datetime.strptime(item, "%Y-%m-%d").weekday()+1 in [6, 7]:
            dates.remove(item)
    base = alt.Chart(source, title="{0}【{1}】工时消耗情况".format(date, name)).encode(
        alt.X(
            field="date",
            sort='ascending',
            timeUnit="yearmonthdate",
            axis={"labelAngle": 15, "title": "date", "titleColor": '#5276A7', "format": "%m-%d", "formatType": "time"},
            scale=alt.Scale(zero=True, domain=dates)
        )
    )
    line = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
        alt.Y(
            'Total:Q',
            axis=alt.Axis(title='hours', titleColor='#5276A7'),
            scale=alt.Scale(zero=True, padding=20)

        )
    )

    text = base.mark_text(dx=-15, dy=2, color='red').encode(
        y=alt.Y('Total:Q'),
        text=alt.Text('Total:Q')
    )

    s = (line+text).interactive().properties(width=1200, height=800)
    altair_viewer.show(s)


if __name__ == "__main__":
    personalWorkHours(" 平台测试", "沈番", "2022-11")



