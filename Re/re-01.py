"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     re-01.py
@Author:   shenfan
@Time:     2022/8/30 14:13
"""
import re

s = "abc123def123def"

pattern = re.compile("([a-z])\d+([a-z])")
result = pattern.findall(s)
results = pattern.finditer(s)
print(result)
for i in results:
    print(i.group(),end="\n")


#findall 遇到分组时返回分组匹配的结果
s = "one,two,three,four"
pattern = re.compile("\W+")
result = pattern.split(s)
print(result)
resultsub = pattern.sub("-",s)
print(resultsub)
print(re.sub("\W+"," ",s))
#split对匹配的结果进行分割
print(re.subn("\W+"," ",s))
print(re.sub("(\w+),(\w+)",r"\2***\1",s))






