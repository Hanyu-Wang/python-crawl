#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/5/13 14:02
# @Author : why
# @File : Project-9APP爬取糗事百科.py
# @Software: PyCharm

import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.114 Safari/537.36',
}


def get_json_data(num):
    url = f'https://m2.qiushibaike.com/article/list/text?page={num}&count=12'
    res = requests.get(url=url, headers=headers).json()
    return res


def analyze_json(json_data):
    items = json_data['items']
    for i in items:
        author = i['user']['login']
        content = i['content']
        result = f'作者：{author}\n糗事：{content}\n\n'
        with open('糗事百科.txt', 'a', encoding='utf-8') as f:
            f.write(result)


if __name__ == '__main__':
    for j in range(1, 6):
        analyze_json(get_json_data(j))
