"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     stacticsInfo.py
@Author:   shenfan
@Time:     2022/11/14 11:30
"""
import pandas
import os
from Xboard.Delivery.deliveryReport.projectInfo import modelProject
from Xboard.Delivery.deliveryReport.deliveryModelInfo import modelInfo
from Xboard.Delivery.deliveryReport.dmsInfo import modelDms
from Xboard.Delivery.deliveryReport.taskInfo import taskInfo
from Xboard.Delivery.deliveryReport.checkDatas import standardDetials


def staticStandard(objectid, projectid):
    rule_dir = os.path.join(os.path.abspath(".."), "datas", "规则引擎数据-审查项(全).xls")
    rule = pandas.read_excel(rule_dir)
    model = modelInfo(objectid).astype(str)
    project = modelProject(projectid).astype(str)
    task = taskInfo(objectid).astype(str)
    dms = modelDms(objectid).astype(str)

    model = pandas.merge(model, dms, on="modelId", how="left")
    base = pandas.merge(task, project, on="project_id", how="left")
    model = pandas.concat([model, base], axis=1)

    standard = standardDetials(objectid)
    major = rule[["rule_code", "审查项", "专业"]].to_dict(orient="records")

    standardMajor = []
    for item in set(standard["audit_page_code"].tolist()):
        for item_standard in major:
            if item in item_standard["rule_code"]:
                standardMajor.append(dict(zip(("audit_page_code", "major"), (item, item_standard["专业"]))))
    standard = pandas.merge(standard, pandas.DataFrame(standardMajor), on="audit_page_code", how="left")

    standard_model = pandas.merge(standard.astype(str), model.astype(str), on="model_id", how="left")

    dirpath = os.path.join(os.path.abspath(".."), "datas")
    writer = pandas.ExcelWriter(os.path.join(dirpath, "Statics.xls"))
    standard_model.to_excel(writer, sheet_name="总览", index=None)
    model.to_excel(writer, sheet_name="技术审查", index=None)
    project.to_excel(writer, sheet_name="项目详情", index=None)
    task.to_excel(writer, sheet_name="任务详情", index=None)
    dms.to_excel(writer, sheet_name="DMS详情", index=None)
    writer.save()
    writer.close()


if __name__ == "__main__":
    staticStandard("893499353765208064", "891756504246358016")
