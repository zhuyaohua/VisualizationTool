"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     examAnalysis_accounts.py
@Author:   shenfan
@Time:     2022/9/2 17:45
"""
import altair as alt
from Xboard.exam_analysis_datas import examAnalysisAcounts
import altair_viewer
import pandas

source = pandas.DataFrame(examAnalysisAcounts(("880449162881212416", "880449895613538304", "880448119040978944"), "843822015721902080"))

base = alt.Chart(source).mark_line(point=True,color="green").encode(
    x=alt.X("user:N", title="Models",axis={"labelAngle": 15}),
    y=alt.Y("acountcounts:Q", title="Accounts")
)

s = base.interactive().properties(width=800, height=200)

altair_viewer.show(s)
