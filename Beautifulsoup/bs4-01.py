"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     bs4-01.py
@Author:   shenfan
@Time:     2022/8/31 9:57
"""
from bs4 import BeautifulSoup
import requests

# 获取页面
r = requests.get("https://www.cbim.org.cn/analysis/").content.decode("UTF-8")

# 解析BeautifulSoup的解析模式有三种：html/xml/html5
soup = BeautifulSoup(r, "html.parser")

# 格式化
html = soup.prettify()

# 四大对象
# 1、标签
print(soup.html.head.meta)
print(soup.div)  # 默认获取soup对象中的第一个div
print(soup.html.input.attrs)  # 获取标签的熟悉attrs

# 2、文本
print(soup.strong.string)

"""
遍历文档数
    1.子节点 contents
"""
print(soup.html.head.contents)
print(soup.html.head.children)
# 节点内容
print(soup.html.strong.text)
print(soup.html.head.contents[5].parent)
print(soup.html.div.next_sibling.next_sibling.attrs)
print(soup.html.div.next_sibling.next_sibling.previous_sibling)

# 查找文档数
print(soup.html.find_all("div"))
