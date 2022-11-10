"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     main.py
@Author:   shenfan
@Time:     2022/10/25 11:02
"""
from gooey import Gooey, GooeyParser

"""
| 控件名        | 控件类型    |

| FileChooser      | 文件选择器 | 
| MultiFileChooser | 文件多选器 | 
| DirChooser       | 目录选择器 |
| MultiDirChooser  | 目录多选器 |
| FileSaver        | 文件保存   |
| DateChooser      | 日期选择   |
| TextField        | 文本输入框 |
| Dropdown         | 下拉列表   |
| Counter          | 计数器     |
| CheckBox         | 复选框     |
| RadioGroup       | 单选框     |
"""


@Gooey
def main():
    parser = GooeyParser(description="测试效率小工具")
    sub_parser = parser.add_subparsers(description="选择模型")
    sub_parser.add_argument("path", help="模型路径", widget="FileChooser")
    sub_parser.add_argument("确认", widget="")
    parser.add_argument("Result", widget="TextField")
    args = parser.parse_args()

    print(args)


main()


