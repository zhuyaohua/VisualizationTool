"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     examAnalysis_account.py
@Author:   shenfan
@Time:     2022/9/2 17:11
"""
import altair as alt
from Xboard.exam_analysis_datas import examAnalysisAcount
import altair_viewer
import pandas

source = pandas.DataFrame(examAnalysisAcount("8a06da6f-1ca1-42f8-b8cd-b7292902ddd6", "843822015721902080"))

base = alt.Chart(source).encode(
    x=alt.X(
        field='operation_time',
        type='nominal',
        timeUnit="utcyearmonthdatehoursminutesseconds",
        axis={"labelAngle": 15},
        title="操作时间",
    )
)

bar = base.mark_bar().encode(y='device_id:N')

line = base.mark_line(point=True, color='red').encode(
    y=alt.Y(
        field="true_name",
        type='nominal',
        title="用户"
    )
)

s = line.interactive().properties(width=800, height=200)

altair_viewer.show(s)



