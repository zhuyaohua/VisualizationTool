"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     Intelligence.py
@Author:   shenfan
@Time:     2022/9/16 10:58
"""
import random
import numpy
import pandas
import altair as alt
import altair_viewer


def generator_randint(n):
    data = []
    for i in range(n):
        sampers = numpy.array([random.randint(1, 100) for i in range(random.randint(1, 100000))])
        temp = {"samper": len(sampers), "agv": sampers.mean()}
        data.append(temp)
    return pandas.DataFrame(data)


source = generator_randint(100)

base = alt.Chart(source).properties(width=900)

line = base.mark_line().encode(x='samper', y='agv')

rule = base.mark_rule().encode(
    y="50",
    size=alt.value(2)
)

altair_viewer.show(line)


