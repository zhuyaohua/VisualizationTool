"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     examAnalysis_devices.py
@Author:   shenfan
@Time:     2022/9/2 15:36
"""
import altair as alt
from Xboard.exam_analysis_datas import examAnalysisDatas
import altair_viewer
import pandas

source = pandas.DataFrame(examAnalysisDatas("8a06da6f-1ca1-42f8-b8cd-b7292902ddd6", "878941069851627520")["设备异常分布"])

base = alt.Chart(source).encode(
    x=alt.X(
        field='operation_time',
        type='temporal',
        sort='descending',
        timeUnit="utcyearmonthdatehoursminutes",
        axis={"labelAngle": 15},
        title="操作时间",
    )
)

bar = base.mark_bar().encode(y='device_id:N')

line = base.mark_line(color='red').encode(
    y=alt.Y(
        field="device_id",
        type='nominal',
        title="设备ID"
    )
)

s = line.interactive().properties(width=600, height=300)

altair_viewer.show(s)
