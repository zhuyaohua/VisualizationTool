"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     lxml-04.py
@Author:   shenfan
@Time:     2022/9/16 9:22
"""
from lxml import etree
import altair as alt
import altair_viewer
import pandas

alt.data_transformers.disable_max_rows()

html = etree.parse(r"C:\Users\SHENFAN\Desktop\result-20220920155443-1.jtl")

ts = html.xpath("//httpSample/@ts")
lb = html.xpath("//httpSample/@lb")


requestTimes = {}
for item in ts:
    requestTimes.setdefault(item, 1)
    requestTimes[item] += 1

source = []
for key, value in requestTimes.items():
    source.append(dict(zip(("Time", "interfaces"), (int(key), value))))
source = pandas.DataFrame(source)

print(source)
line = alt.Chart(source).mark_line(color="green").encode(
    x=alt.X(
        field='Time',
        type='temporal',
        sort='ascending',
        timeUnit="yearmonthdatehoursminutesseconds",
        axis={"labelAngle": 15},
        title="时间"
    ),
    y=alt.Y("sum(interfaces):Q", title="interfaces/s")
)

altair_viewer.show(line.interactive().properties(width=1500, height=600))
