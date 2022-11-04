"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     bs4-02.py
@Author:   shenfan
@Time:     2022/8/31 11:30
"""
from bs4 import BeautifulSoup
import requests
import re

html = requests.get("https://testerhome.com/").content.decode("UTF-8")
soup = BeautifulSoup(html, "html.parser")

links = soup.html.find_all(href=re.compile("^https:.*"))
datas = []
for item in links:
    print(item.attrs["href"])
links = soup.find_all(class_="title media-heading")
for item in links:
    text = []
    temp_soup = BeautifulSoup(
        requests.get("https://testerhome.com/" + item.find(name="a").attrs["href"]).content.decode("UTF-8"),
        "html.parser")
    with open("text.txt","w+",encoding="utf-8") as filestream:
        filestream.write(str(temp_soup.find_all("p")))