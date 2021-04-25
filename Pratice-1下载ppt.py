#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/25 13:43
# @Author : why
# @File : Pratice-1下载ppt.py
# @Software: PyCharm
"""
爬取http://www.pptbz.com/pptmoban/jingmeippt/页所有的PPT模板
"""
import requests
import os
from lxml import etree
from retry import retry

index_url = 'http://www.pptbz.com/pptmoban/jingmeippt/'
base_url = 'http://www.pptbz.com/'

# 创建文件夹
folder = './ppt模板'
if not os.path.exists(folder):
    os.makedirs(folder)


# 获取ppt后缀
def get_suffix(link):
    suffix = link.split('.')[-1]
    return suffix


# 获取PPT元素的集合
def get_ppt_element(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36',
    }

    response = requests.get(url, headers=headers)
    # print(response.text)
    response.encoding = 'gbk'
    tree = etree.HTML(response.text)
    elements = tree.xpath("//div[@class='wrapper']/ul/li")

    return elements


# 获取ppt下载链接
def get_download_link(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36',
    }

    response = requests.get(url, headers=headers)
    # print(response.text)
    response.encoding = 'gbk'
    tree = etree.HTML(response.text)
    download_url = tree.xpath("//div[@class='button']/a/@href")
    download_type = get_suffix(*download_url)
    return download_url, download_type


# 下载PPT
@retry(tries=10, delay=2000)  # 通过retry装饰器实现如果出错就重启10次，每次间隔2秒。
def download_ppt(p_name, p_link, p_type):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36',
        'referer': 'http://www.pptbz.com/'
    }
    r = requests.get(p_link, headers=headers)
    data = r.content
    file_name = f'{folder}/{p_name}.{p_type}'
    with open(file_name, 'wb')as f:
        f.write(data)


if __name__ == '__main__':
    for li in get_ppt_element(index_url):
        ppt_name = li.xpath('./a[2]/text()')[0]
        ppt_url = li.xpath('./a[2]/@href')[0]
        full_link = f'{base_url}{ppt_url}'
        ppt_link, ppt_type = get_download_link(full_link)
        print(f'正在下载{ppt_link}')
        download_ppt(ppt_name, full_link, ppt_type)
    print("全部下载完成")
