#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/5/12 14:00
# @Author : why
# @File : Project-7异步爬虫.py
# @Software: PyCharm
import time
import requests
from lxml import etree
from multiprocessing.dummy import Pool

# 通过线程池下载简历
index_url = 'https://sc.chinaz.com/jianli/free.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42',
}


# 因为本次项目需要先请求目录页，再请求详情页，最后再请求文件下载链接，可能还要实现翻页
# 所以封装一个函数，方便重复使用
def request(url):
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r
        else:
            print('Non 200 status code')
            return ''
    except Exception as err:
        print('crawler error：' + err)


# 爬取目录页中详情页的url。
def get_detail_link(url):
    response = request(url)
    tree = etree.HTML(response.text)
    detail_link = tree.xpath('//*[@id="container"]/div/p/a/@href')
    detall_link_list = ['https:' + i for i in detail_link]  # url拼接
    return detall_link_list


def download_document(url):
    r = request(url)
    tree = etree.HTML(r.content.decode('utf-8'))
    document_name = tree.xpath('//h1/text()')[0]
    document_link = tree.xpath('//*[@id="down"]/div[2]/ul/li[1]/a/@href')[0]
    document_type = document_link[-3:]
    document_content = request(document_link)
    print(f"开始下载{document_name}。")
    with open(f'{document_name}.{document_type}', 'wb')as f:
        f.write(document_content.content)
    print(f"{document_name}下载结束！")


def run():
    with Pool(10) as pool:
        pool.map(download_document, get_detail_link(index_url))


if __name__ == '__main__':
    start_time = time.time()
    run()
    end_time = time.time()
    print(f'共用时：{end_time - start_time}')
