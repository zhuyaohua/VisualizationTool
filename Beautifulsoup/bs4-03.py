"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     bs4-03.py
@Author:   shenfan
@Time:     2022/9/6 15:17
"""
from bs4 import BeautifulSoup
from lxml import etree
import requests

html = requests.get("https://test-gw.cbim.org.cn/doc.html#/home").content.decode("UTF-8")
soup = BeautifulSoup(html, "lxml")
html = soup.prettify()
print(html)
print(soup.select("link"))
print(soup.select("div[id]")[0].attrs["id"])

print("*"*100)

htmle = etree.HTML(html)
htmles = etree.tostring(htmle, pretty_print=True, encoding="UTF-8").decode("UTF-8")
dom = htmle.xpath("//div/@id")
print(dom)

