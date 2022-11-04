"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     get_session.py
@Author:   shenfan
@Time:     2022/9/2 10:33
"""
import requests
import re


def get_cbim_session_key(host: str, username: str, passwd: str):
    url = f'{host}/cas/login?service={host}/app'
    r = requests.get(url)
    # 加密字符串
    execution = re.search('name="execution" value="(.*?)"', r.text, re.S).groups(1)[0]
    # cookie
    session_temp = r.headers['Set-Cookie']
    session_temp = re.search('SESSION=(.*?);', session_temp, re.S).groups(1)[0]
    r = requests.request(
        'post',
        url,
        headers={
            'cookie': f'SESSION={session_temp}',
        },
        data={
            'username': username,
            'password': passwd,
            'verifyCode': None,
            'execution': execution,
            '_eventId': 'submit',
            'loginMode': '2'
        },
        allow_redirects=False
    )
    # 重定向地址
    location = r.headers['Location']
    r = requests.get(location, allow_redirects=False)
    session = re.search('CBIM-SESSION=(.*?);', r.headers['Set-Cookie'], re.S).groups(1)[0]
    return session



