"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     data_output.py
@Author:   shenfan
@Time:     2022/9/2 10:35
"""
import pandas
import os
from datetime import datetime
from styleframe import StyleFrame


def savefile(data, filename, outputdir, filetype="csv"):
    dataframe = pandas.DataFrame(data, index=None)
    pandas.set_option('display.float_format', lambda x: '%.2f' % x)
    if filetype == "csv":
        dataframe.to_csv(os.path.join(outputdir, filename), index=False, decimal=".", encoding="utf-8",
                         float_format='%.0f')
    if filetype == "xls":
        # excel_writer = StyleFrame.ExcelWriter(os.path.join(outputdir, filename))
        # sf = StyleFrame(dataframe)
        # sf.to_excel(
        #     excel_writer=excel_writer,
        #     best_fit=dataframe.columns.tolist(),
        #     columns_and_rows_to_freeze='B2',
        #     row_to_add_filters=0,
        # )
        # excel_writer.save()
        dataframe.to_excel(os.path.join(outputdir, filename), index=False, sheet_name=datetime.strftime(datetime.now(),"%Y%m%d"))


