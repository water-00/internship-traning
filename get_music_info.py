# 导入所需模块
import requests
from lxml import etree
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import csv #调用数据保存文件
import pandas as pd #用于数据输出

import time
import re
import random


def get_info(url):
    # 创建一个浏览器实例
    driver = webdriver.Chrome()

    # 打开目标网页
    driver.get(url)

    # 使用XPath定位链接文本的元素
    link_element = driver.find_element(By.XPATH, '//*[@id="div1"]/table/tbody/tr[1]/td[1]/a[4]/b')

    # 点击链接
    link_element.click()

    # 获取操作完成后的页面源代码
    wait = WebDriverWait(driver, 10)  # 最长等待时间为10秒
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))  # 等待<body>元素出现
    page_source = driver.page_source

    selector = etree.HTML(page_source)
    author_name = selector.xpath('//*[@id="widthsetter"]/table[1]/tbody/tr/td[3]/h1/text()')[0].strip()
    print("作曲家：" + author_name)
    author_life = selector.xpath('//*[@id="widthsetter"]/table[1]/tbody/tr/td[3]/text()')[0].strip()
    print("生卒年：" + author_life)
    for i in range(20):
        print("rank:", i + 1)
        temp_path = '//*[@id="div1"]/table/tbody/tr[{}]/td[1]/i/text()'.format(i + 2)
        temp = selector.xpath(temp_path)[0].strip()
        match = re.match(r"\((\d+);(\d+)m\)", temp)
        if match:
            version = match.group(1)
            duration = match.group(2) + 'm'
            print("versions:", version)
            print("duration:", duration)
        else:
            print("未找到匹配的内容")
        name_path = '//*[@id="div1"]/table/tbody/tr[{}]/td[1]/a/text()'.format(i + 2)
        name = selector.xpath(name_path)[0].strip()
        print("name:" + name)
        opus_path = '//*[@id="div1"]/table/tbody/tr[{}]/td[2]/text()'.format(i + 2)
        opus = selector.xpath(opus_path)[0].strip()
        print("opus:" + opus)
    # 关闭浏览器实例
    driver.quit()


if __name__ == '__main__':
    url = 'https://www.classiccat.net/beethoven_l_van/index.php'
    get_info(url)
    print("End....")