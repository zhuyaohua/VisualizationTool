"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     examAnalysis_compentsrate.py
@Author:   shenfan
@Time:     2022/9/2 16:29
"""
import altair as alt
from Xboard.exam_analysis_datas import examAnalysisDatas
import altair_viewer
import pandas

data = examAnalysisDatas("b193ea04-2161-44a5-b633-ce913af25215-CF", "871720647447941120")
temp = {"原创构件数": data["原创构件数"], "非原创构件数": data["非原创构件数"]}
datas = []
for itemkey, itemvalue in temp.items():
    datas.append(dict(zip(("counts", "site", "type"), (itemvalue, itemkey, "rates"))))

source = pandas.DataFrame(datas)

bars = alt.Chart(source).mark_bar().encode(
    x=alt.X('sum(counts):Q', stack='zero'),
    y=alt.Y('type:N'),
    color=alt.Color('site')
)

text = alt.Chart(source).mark_text(dx=-15, dy=3, color='white').encode(
    x=alt.X('sum(counts):Q', stack='zero', title="counts"),
    y=alt.Y('type:N', title="构件类型"),
    detail='site:N',
    text=alt.Text('sum(counts):Q', format='.1f')
)

s = (bars + text).interactive()

altair_viewer.show(s)
