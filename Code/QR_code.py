"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     QR_code.py
@Author:   shenfan
@Time:     2022/11/4 16:17
"""
from MyQR import myqr

myqr.run(words="Tell Phone:13924274331",
         version=3,
         picture=r"C:\Users\SHENFAN\Pictures\Saved Pictures\八万 (2).jpg",
         colorized=True,
         save_name="P1.png")


import qrcode
from io import BytesIO

#
# def QRcode(data):
#     qr = qrcode.QRCode(
#         version=2,  # 尺寸大小
#         error_correction=qrcode.constants.ERROR_CORRECT_L,  # 容错系数 ERROR_CORRECT_L: 7%的字码可被容错
#                                                             # ERROR_CORRECT_M: 15%的字码可被容错
#                                                             # ERROR_CORRECT_Q: 25%的字码可被容错
#                                                             # ERROR_CORRECT_H: 30%的字码可被容错
#         box_size=10,
#         border=1
#     )
#     qr.add_data(data)
#     qr.make(fit=False)
#     img = qr.make_image()
#     buf = BytesIO()
#     img.save(buf)
#     image_stream = buf.getvalue()
#     with open("二维码.png", "wb+") as file:
#         file.write(image_stream)
#     return image_stream
#
#
# QRcode("13924274331")


