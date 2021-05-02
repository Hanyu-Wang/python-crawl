#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/5/2 20:53
# @Author : why
# @File : P6-代理IP-2.py
# @Software: PyCharm
import random
import requests


class HSpider:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36',
    }
    ip_pool = ''

    @property
    def proxy(self):
        ip = requests.get(url=self.ip_pool).text.strip()
        print(ip)
        return {'http': f'https://{ip}'}

    def __init__(self, n):
        self.n = n

    def get_links(self):
        urls = []
        for i in range(1, self.n + 1):
            urls.append(f'https://db.yaozh.com/hmap/{i}.html')
        random.shuffle(urls)
        return urls

    def get_data(self, url):
        res = requests.get(url=url, headers=self.headers, proxies=self.proxy, allow_redirects=False)
        print('当前请求的链接：', res.url)
        print('当前返回的响应码：', res.status_code)
        print('================================================')

    def run(self):
        links = self.get_links()
        for h_url in links:
            self.get_data(h_url)


if __name__ == '__main__':
    spider = HSpider(10)
    spider.run()
