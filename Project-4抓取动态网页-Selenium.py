#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/27 20:49
# @Author : why
# @File : P4-抓取动态网页-2.py
# @Software: PyCharm

from lxml import etree
import time
from selenium import webdriver

driver = webdriver.Chrome()


def extract_data(page_source):
    tree = etree.HTML(page_source)
    book_list = tree.xpath("//div[@id='bookItem']/a")
    for i in book_list:
        book_name = i.xpath("./div[2]/text()")[0]
        book_price = i.xpath("./div[3]/div[1]/text()")[0]
        print(f'{book_name}价格为{book_price}')


def get_next_page():
    next_page = driver.find_element_by_xpath("//div[@class='list-pagination']//button[2]")
    next_page.click()


def get_data():
    for _ in range(10):
        extract_data(driver.page_source)
        time.sleep(1)
        get_next_page()
        time.sleep(2)


if __name__ == '__main__':
    driver.get('https://www.epubit.com/books')
    get_data()
    driver.close()
