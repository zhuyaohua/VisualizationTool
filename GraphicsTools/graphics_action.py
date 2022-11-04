"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     graphics_action.py
@Author:   shenfan
@Time:     2022/8/10 17:42
"""
import altair
import altair_viewer
from vega_datasets import data
import pandas


class graphics:
    def __init__(self, dataframe: pandas.DataFrame):
        self.source = dataframe

    #柱状图
    def histogram(self, width=1600, height=900):
        altair.Chart(self.source).mark_bar().encode(x='a', y='b')

from DataTools.json_extractor import extractor
import os
import json

with open(os.path.join(os.path.dirname(os.path.abspath(".")), "Data", "Data.json"), "r", encoding="utf-8") as file:
    datas = json.loads(file.read())

dataframe = extractor(datas,"$.result..*[?(@.code != None)]", "code", "ruleLibCode","menuShowDes")
dataframe = pandas.DataFrame(dataframe,index=None)
char = altair.Chart(dataframe)
alt=char.mark_bar(color="red").encode(
    x=altair.X("ruleLibCode:N",title="category"),
    y=altair.Y("count()",title="总数"),
    color="名称:N"
).interactive().properties(width=1600, height=900)
altair_viewer.show(alt)
alt.save("char.html")