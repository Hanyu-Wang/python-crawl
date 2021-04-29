#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/29 20:29
# @Author : why
# @File : Project-5模拟登录.py
# @Software: PyCharm
"""
通过第三方图鉴网平台实现对古诗文网站的模拟登录
"""
import base64
import json
import requests

tujian_url = 'http://www.ttshitu.com/'


# 把图鉴网给的python库封装成一个类
class tujian:
    def __init__(self, typeid=3):
        self.uname = 'dongtiandeyu'
        self.pwd = 'why123456'
        self.typeid = typeid

    def get_code(self, img_path):
        with open(img_path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            b64 = base64_data.decode()
        data = {"username": self.uname, "password": self.pwd, "typeid": self.typeid, "image": b64}
        result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
        if result['success']:
            return result["data"]["result"]
        else:
            return result["message"]


# 实例化一个session网页会话
r = requests.session()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.114 Safari/537.36',
}
# 先获得验证码图片
response = r.get('https://so.gushiwen.cn/RandCode.ashx', headers=headers)

with open('验证码.png', 'wb')as f:
    f.write(response.content)
# 把获取到的验证码图片调用图鉴网封装的类实现自动识别
captcha = tujian().get_code(r'验证码.png')
data = {
    '__VIEWSTATE': 'XH67ib6mjeNG03E080ON6QoiYh8A2GUCx4SsA0tcB2RRPqt10hLwnQR204kbTI+V'
                   '/WqkZQocRvh9KTGKj5ENchtLyPdENydaArB+F+2g0PZS5JfiNgqLec643/c=',
    '__VIEWSTATEGENERATOR': 'C93BE1AE',
    'from': '',
    'email': '75758347@qq.com',
    'pwd': 'why123.00',
    'code': captcha,
    'denglu': '登录'
}
print(f'识别验证码为： {captcha}')
# 向网站服务器发起post请求
r = r.post('https://so.gushiwen.cn/user/login.aspx', headers=headers, data=data)

# 获得登录后的页面
with open('index.html', 'w', encoding="utf-8")as fp:
    fp.write(r.text)
    print('成功登录，并获取网页！')
