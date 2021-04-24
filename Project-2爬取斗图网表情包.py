#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/21 20:19
# @Author : why
# @File : P2-爬取斗图网表情包.py
# @Software: PyCharm
import requests
from lxml import etree
import os

# 创建文件夹
folder = './images'
if not os.path.exists(folder):
    os.makedirs(folder)


def get_pic_element():
    index_url = 'https://www.doutub.com/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36',
    }

    response = requests.get(index_url, headers=headers)
    # print(response.text)
    tree = etree.HTML(response.text)
    elements = tree.xpath("//div[@class='recommend-expression']/div/div")
    return elements


def download_pic(p_name, p_link, p_type):
    '''
      :url 表情包的url,
      :pic_name 表情包的名字,
      :suffix 表情包文件的后缀
    '''
    print(f'downloading {p_link}')
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36',
        'referer': 'https://www.doutub.com/'
    }
    r = requests.get(p_link, headers=headers)
    data = r.content
    file_name = f'{folder}/{p_name}.{p_type}'
    with open(file_name, 'wb')as f:
        f.write(data)


if __name__ == '__main__':
    for div in get_pic_element():
        pic_name = div.xpath("./a/span/text()")[0]
        pic_link = div.xpath("./a/img/@src")[0]
        pic_type = pic_link[-3:]
        download_pic(pic_name, pic_link, pic_type)
