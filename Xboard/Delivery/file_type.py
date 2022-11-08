"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     file_type.py
@Author:   shenfan
@Time:     2022/10/17 10:28
"""
import filetype
import zipfile
import os

base_dir = os.path.abspath(".")
unzip_dir = os.path.join(base_dir, "unzipfiles")


def unzip(filepath, filename):
    file = os.path.join(filepath, filename)
    if zipfile.is_zipfile(file):
        with zipfile.ZipFile(file=file, mode='r') as zf:
            unzipfile = os.path.join(unzip_dir, filename[:-4])
            if not os.path.exists(unzipfile):
                os.mkdir(unzipfile)
                for old_name in zf.namelist():
                    file_size = zf.getinfo(old_name).file_size
                    new_name = old_name.encode('cp437').decode('gbk')
                    new_path = os.path.join(unzipfile, new_name)
                    if file_size > 0:
                        with open(file=new_path, mode='wb') as f:
                            f.write(zf.read(old_name))
                    else:
                        os.mkdir(new_path)
    else:
        print("%s %s文件类型不支持" % (filename, filetype.guess(file).extension))
    return unzipfile


if __name__ == "__main__":
    unzip(r"C:\Users\SHENFAN\Desktop\中设数字\企业微信\WXWork\1688853067030957\Cache\File\2022-11", "新琼小学BIM模型_建筑20221102.jdm")






