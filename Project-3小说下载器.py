#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/24 17:06
# @Author : why
# @File : P3-小说下载器.py
# @Software: PyCharm

import requests
from lxml import etree
import os
from retry import retry

index_url = 'https://www.tsxs.org/16/16814/'
base_url = 'https://www.tsxs.org'


def mkfolder(folder_name):
    if not os.path.exists(folder_name):
        print('文件夹不存在，先创建文件夹')
        os.makedirs(folder_name)
    # 切换到文件中
    os.chdir(folder_name)


def get_novel_name(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36',
    }

    response = requests.get(url, headers=headers)
    # print(response.text)
    response.encoding = 'gbk'
    tree = etree.HTML(response.text)
    name = tree.xpath("//div[@id='maininfo']/div[1]/h1/text()")[0]
    print(f'小说的名字是{name}')
    return name


# 抓取小说目录
def get_catalogue(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36',
    }

    response = requests.get(url, headers=headers)
    response.encoding = 'gbk'
    tree = etree.HTML(response.text)

    chapter = tree.xpath("//*[@id='chapterlist']/li/a/text()")
    link = tree.xpath("//*[@id='chapterlist']/li/a/@href")
    catalog = list(zip(chapter, link))
    return catalog


# 实现一个章节内容的抓取
@retry(tries=10, delay=2000)  # 通过retry装饰器实现如果出错就重启10次，每次间隔2秒。
def get_content(url):
    content_full = ''
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36',
    }

    response = requests.get(url, headers=headers)
    response.encoding = 'gbk'
    tree = etree.HTML(response.text)
    title = tree.xpath('//*[@id="mains"]/div[1]/h1/text()')[0]
    content = tree.xpath('//*[@id="book_text"]//text()')
    # 将返回的列表转化成字符串，strip()方法去除元素左右的空格或回车
    # content = ('\n'.join([i.strip() for i in content]))
    for i in content:
        a = i.strip()
        content_full = content_full + a
    content = '\n'.join(content_full)
    return title, content


# 将抓取的内容写入文件中
def save_file(title, content):
    print(title + "开始保存")
    with open(f'{title}.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print(title + '保存成功')


def run_spider():
    novel_name = get_novel_name(index_url)
    mkfolder(f'./{novel_name}')
    novel_catalog = get_catalogue(index_url)
    for _, link in novel_catalog:
        full_link = f'{base_url}{link}'
        catalog_title, novel_content = get_content(full_link)
        save_file(catalog_title, novel_content)
    print("整本小说下载完成")


if __name__ == '__main__':
    run_spider()
