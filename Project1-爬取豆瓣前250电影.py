#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/20 14:38
# @Author : why
# @File : 爬取豆瓣前250电影-3.py
# @Software: PyCharm
import requests
from lxml import etree
import pprint

home_page_url = 'https://movie.douban.com/top250'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.114 Safari/537.36',
}


def crawl_one_page(url):
    print(f"开始抓取：{url}")
    response = requests.get(url, headers=headers)
    tree = etree.HTML(response.text)
    rank = tree.xpath('//div[@class="item"]/div[1]/em/text()')
    title = tree.xpath('//div[@class="item"]/div[2]/div[1]/a/span[1]/text()')
    score = tree.xpath('//div[@class="item"]/div[2]/div[2]/div/span[2]/text()')
    next_page = tree.xpath('//span[@class="next"]/a/@href')
    movie_info = list(zip(rank, title, score))
    print("抓取当前页面完成")
    return movie_info, next_page


movies = []
current_url = home_page_url
while current_url:
    movie_info_list, next_page_list = crawl_one_page(current_url)
    movies.append(movie_info_list)
    if len(next_page_list) > 0:
        current_url = f"{home_page_url}{next_page_list[0]}"
    else:
        print("没有下一页了，全部抓取完成")
        current_url = False
pprint.pprint(movies)
