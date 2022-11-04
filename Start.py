"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     Start.py
@Author:   shenfan
@Time:     2022/7/27 15:34
"""
# import altair as alt
# import altair_viewer
#
# # load a simple dataset as a pandas DataFrame
# from vega_datasets import data
# cars = data.cars()
#
# l = alt.Chart(cars).mark_point().encode(
#     x='Horsepower',
#     y='Miles_per_Gallon',
#     color='Origin'
# ).interactive().properties(width=1600, height=800)
# altair_viewer.show(l)

import altair as alt
from vega_datasets import data
import altair_viewer

source = data.movies.url

l=alt.Chart(source).mark_bar().encode(
    alt.X("IMDB_Rating:Q", bin=True),
    y='count()',
).interactive().properties(width=1600, height=900)


import altair as alt
from vega_datasets import data
cars = data.cars()
base = alt.Chart(cars).mark_point().encode(
    x='Horsepower:Q',
    y='Miles_per_Gallon:Q',
).properties(
    width=150,
    height=150
)

s=alt.vconcat(
    base.encode(color='Cylinders:Q').properties(title='quantitative'),
    base.encode(color='Cylinders:O').properties(title='ordinal'),
    base.encode(color='Cylinders:N').properties(title='nominal'),
)

altair_viewer.show(s)