"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     lxml-03.py
@Author:   shenfan
@Time:     2022/9/15 15:39
"""
import requests
from bs4 import BeautifulSoup
import re

base_html = requests.get("https://www.zhipin.com/web/geek/job").content.decode("utf-8")

soup = BeautifulSoup(base_html, "html.parser")
print(soup.prettify())
