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


music_data = []


def read_csv(path):
    names = []
    with open(path, 'r', encoding='utf-8') as file:
        # 创建CSV读取器
        reader = csv.reader(file)
        next(reader)
        # 逐行读取CSV文件内容并打印
        for row in reader:
            names.append(row[0])
        names = list(set(names))
        return names


def get_urls(name):
    name = name.lower()
    last_name, first_name = name.split(',')
    first_name_initials = first_name.split()
    url = last_name + "_"
    for word in first_name_initials:
        url = url + word[0]
    url_final = "https://www.classiccat.net/" + url + "/index.php"
    print(url_final)
    get_info(url_final)


def get_info(url):
    # 创建一个浏览器实例
    driver = webdriver.Chrome()

    # 打开目标网页
    driver.get(url)
    # 网页不存在
    if "Error" in driver.title:
        print(f"url不存在: {url}")
        return
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
        # 曲名
        name_path = '//*[@id="div1"]/table/tbody/tr[{}]/td[1]/a/text()'.format(i + 2)
        # 作品数不满20
        if selector.xpath(name_path) == []:
            break
        name = selector.xpath(name_path)[0].strip()
        print("name:" + name)
        # 排名
        rank = i + 1
        print("rank:", rank)
        # 版本数和时长
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
        # opus
        opus_path = '//*[@id="div1"]/table/tbody/tr[{}]/td[2]/text()'.format(i + 2)
        opus = selector.xpath(opus_path)[0].strip() if selector.xpath(opus_path) != [] else ''
        print("opus:" + opus)
        data = [rank, name, opus, version, duration, author_name, author_life]
        music_data.append(data)
    # 不满20的继续读页面右边一列
    if i != 19:
        curr_rank = i
        i = 0
        for temp in range(curr_rank, 20):
            # 曲名
            name_path = '//*[@id="div2"]/table/tbody/tr[{}]/td[1]/a/text()'.format(i + 2)
            # 作品数不满20
            if selector.xpath(name_path) == []:
                break
            name = selector.xpath(name_path)[0].strip()
            print("name:" + name)
            # 排名
            rank = temp + 1
            print("rank:", rank)
            # 版本数和时长
            temp_path = '//*[@id="div2"]/table/tbody/tr[{}]/td[1]/i/text()'.format(i + 2)
            temp = selector.xpath(temp_path)[0].strip()
            match = re.match(r"\((\d+);(\d+)m\)", temp)
            if match:
                version = match.group(1)
                duration = match.group(2) + 'm'
                print("versions:", version)
                print("duration:", duration)
            else:
                print("未找到匹配的内容")
            # opus
            opus_path = '//*[@id="div2"]/table/tbody/tr[{}]/td[2]/text()'.format(i + 2)
            opus = selector.xpath(opus_path)[0].strip() if selector.xpath(opus_path) != [] else ''
            print("opus:" + opus)
            data = [rank, name, opus, version, duration, author_name, author_life]
            music_data.append(data)
            i += 1
    # 关闭浏览器实例
    driver.quit()


def write_data_to_csv(columns, datas):
    test = pd.DataFrame(columns=columns, data=datas)  # 将数据放进表格
    test.to_csv('music_data.csv')  # 数据存入csv,存储位置及文件名称


if __name__ == '__main__':
    path = 'musicians_relationships_eng.csv'
    composer_list = read_csv(path)
    for composer in composer_list:
        get_urls(composer)
    print(music_data)
    print("开始写入csv。。。")
    header = ['rank', 'name', 'opus', 'versions', 'duration', 'composer_name', 'composer_life']
    write_data_to_csv(header, music_data)
    print("End....")