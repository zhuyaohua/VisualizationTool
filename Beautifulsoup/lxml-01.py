"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     lxml-01.py
@Author:   shenfan
@Time:     2022/9/5 13:47
"""
from lxml import etree
import requests

html = requests.get("https://kaifa.baidu.com").content.decode("UTF-8")

html = etree.HTML(html)
result = etree.tostring(html, pretty_print=True, encoding="UTF-8").decode("UTF-8")
dom = html.xpath("//table//td//a/@href")
print(dom)
