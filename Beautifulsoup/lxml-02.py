"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     lxml-02.py
@Author:   shenfan
@Time:     2022/9/15 13:38
"""
from lxml import etree
import requests
from bs4 import BeautifulSoup
import re
import os

output_dir = os.path.join(os.path.dirname(os.path.abspath(".")), "Data", "outputfile")

raw = requests.get("https://blog.51cto.com/").content.decode("utf-8")
lxml_html = etree.HTML(raw)
soup_html = BeautifulSoup(raw, "html.parser")

pre_html = etree.tostring(lxml_html, pretty_print=True, encoding="utf-8").decode("utf-8")

links = lxml_html.xpath("//h2/a/@href")
link = soup_html.find_all(href=re.compile(".*\/python"))

article_links = []

for item in link:
    hit_link = item.attrs["href"]
    hit_raw = requests.get(hit_link).content.decode("utf-8")
    hit_html = etree.HTML(hit_raw)
    article_link = hit_html.xpath("//a[@title]/@href")
    article_links.extend(article_link)

for article in article_links:
    article_content = requests.get(article).content.decode("utf-8")
    hit_article_html = etree.HTML(article_content)
    filename = hit_article_html.xpath("//div/div[@class='title']/h1/text()")[0].strip("?").strip("|")


    with open(os.path.join(output_dir,filename),"w+",encoding="utf-8") as stream:
        for item in hit_article_html.xpath("//div/div[@class='title']/../descendant::*/text()"):
            stream.write(item)


