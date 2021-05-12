#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/5/3 10:16
# @Author : why
# @File : Pratice-2模拟登录招标采购网.py
# @Software: PyCharm
"""
模拟登录https://www.okcis.cn/login/招标采购网
"""
import time

from PIL import Image
from selenium import webdriver
import requests
import base64
import json

tujian_url = 'http://www.ttshitu.com/'


# 把图鉴网给的python库封装成一个类
class Tujian:
    def __init__(self, typeid=1005):
        self.uname = 'xxx'
        self.pwd = 'xxx'
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


if __name__ == '__main__':
    url = 'https://www.okcis.cn/login/'
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(10)
    # 需要根据你电脑的缩放与布局种比例进行调整
    driver.execute_script('document.body.style.zoom="0.8"')
    time.sleep(1)

    # 获取验证码位置	  截图起点（x，y）  验证码大小（width，height）
    element = driver.find_element_by_id('setcode')
    # 截取整个网页
    driver.get_screenshot_as_file('screenshot.png')
    x = element.location['x']
    y = element.location['y']
    right = x + element.size['width']
    bottom = y + element.size['height']
    # 通过Image处理图像
    im = Image.open('screenshot.png')
    im = im.crop((x, y, right, bottom))
    im.save('code.png')
    driver.find_element_by_id('uname').send_keys('xxx')
    driver.find_element_by_id('pwd').send_keys('xxx')
    captcha = Tujian().get_code(r'code.png')
    driver.find_element_by_id('yzm').send_keys(captcha)
    # 再把浏览器调整为原有大小，要不然找不到submit元素
    driver.execute_script('document.body.style.zoom="1"')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="ptlogin"]/tbody/tr[8]/td/input').click()
    time.sleep(3)
    driver.quit()
