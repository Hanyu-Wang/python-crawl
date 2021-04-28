#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/26 20:41
# @Author : why
# @File : P4-抓取动态网页-1.py
# @Software: PyCharm

import requests


def get_book_info(page_num):
    url = 'https://www.epubit.com/pubcloud/content/front/portal/getUbookList'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',  # 头部信息中带上这个参数，假装是ajax去请求的。
        'Origin-Domain': 'www.epubit.com',  # 最好也这个参数也带上，说明自己的来源
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.72 Safari/537.36',
    }

    params = (
        ('page', page_num),  # 页码1，我们只要改变这个参数（1~10）就能获得书籍的数据了
        ('row', '20'),
        ('', ''),
        ('startPrice', ''),
        ('endPrice', ''),
        ('tagId', ''),
    )

    response = requests.get(url=url, headers=headers,
                            params=params).json()  # 我们将这里的text改成json(),让response直接返回python中的字典格式
    return response


def extract_data(json):
    books_list = json['data']['records']
    for i in books_list:
        print(f"书名：{i['name']},价格：{i['price']}")


def get_data():
    for page_num in range(1, 11):
        json_data = get_book_info(page_num)
        extract_data(json_data)


if __name__ == '__main__':
    get_data()
