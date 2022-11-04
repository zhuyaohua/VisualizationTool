"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     main.py
@Author:   shenfan
@Time:     2022/10/25 11:02
"""
from gooey import Gooey, GooeyParser


@Gooey
def main():
    parser = GooeyParser(description="测试效率小工具")
    parser.add_argument("path", help="模型路径", widget="FileChooser")
    args = parser.parse_args()
    print(args)


main()


