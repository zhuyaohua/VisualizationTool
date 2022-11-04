"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     visual_table.py
@Author:   shenfan
@Time:     2022/10/18 11:35
"""
from plotly import graph_objects
from typing import List


def table(Headers: list, Values: List[list]):
    headerColor = 'lightblue'
    rowCheckColor = 'lightgrey'
    rowResultColor = 'salmon'
    fillColor = [rowCheckColor]*(len(Headers)-1)
    fillColor.extend([rowResultColor])
    fmtHeaders = ["<b>{0}</b>".format(item) for item in Headers]
    layout = dict(autosize=True)
    fig = graph_objects.Figure(data=[graph_objects.Table(
        header=dict(
            values=fmtHeaders,
            line_color='darkslategray',
            fill_color=headerColor,
            align=['left', 'center'],
            font=dict(color='Black', size=16)
        ),
        cells=dict(
            values=Values,
            line_color='darkslategray',
            fill_color=fillColor,
            align=['left', 'center'],
            font=dict(color='darkslategray', size=12)
        ))
    ],
        layout=layout)

    fig.show()



