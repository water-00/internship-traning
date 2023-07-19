# 导入所需模块
import requests
from lxml import etree
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import pandas as pd

import time
import re
import random

music_data = []

## 一个从网站上爬取对应音乐家作品的爬虫程序

def read_csv(path):  # 读取关系csv文件，获取需要爬取的作曲家列表
    names = []
    with open(path, 'r', encoding='utf-8') as file:
        # 创建CSV读取器
        reader = csv.reader(file)
        next(reader)
        # 逐行读取CSV文件内容中的作曲家姓名信息
        for row in reader:
            names.append(row[0])
            names.append(row[1])
        names = list(set(names))  # 去重
        return names


def get_urls(name):  # 定位每个人对应的网址
    name = name.lower()
    last_name, first_name = name.split(',')
    first_name_initials = first_name.split()
    url = last_name + "_"
    for word in first_name_initials:
        url = url + word[0]
    url_final = "https://www.classiccat.net/" + url + "/index.php"  # 根据目标网站的url命名规则将作曲家姓名转化成对应url
    print(url_final+" "+name)
    get_info(url_final)  # 分别获取每一个作曲家页面的曲目信息


def get_info(url):  # 提取每一个作曲家页面的曲目信息（动态页面爬取）
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

    # 点击文本，让页面按照受欢迎程度排序
    link_element.click()

    # 获取操作完成后的页面源代码
    wait = WebDriverWait(driver, 10)  # 最长等待时间为10秒
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))  # 等待<body>元素出现
    page_source = driver.page_source

    # 使用xpath方法提取对应数据
    selector = etree.HTML(page_source)
    author_name = selector.xpath('//*[@id="widthsetter"]/table[1]/tbody/tr/td[3]/h1/text()')[0].strip()
    print("作曲家：" + author_name)
    author_life = selector.xpath('//*[@id="widthsetter"]/table[1]/tbody/tr/td[3]/text()')[0].strip()
    print("生卒年：" + author_life)

    # 获取该作曲家前20首热门曲目
    for i in range(20):
        # 曲名
        name_path = '//*[@id="div1"]/table/tbody/tr[{}]/td[1]/a/text()'.format(i + 2)
        # 作品数不满20
        if not selector.xpath(name_path):
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
        # opus编号
        opus_path = '//*[@id="div1"]/table/tbody/tr[{}]/td[2]/text()'.format(i + 2)
        opus = selector.xpath(opus_path)[0].strip() if selector.xpath(opus_path) != [] else ''  # 网页中缺少opus，后续查找补充
        print("opus:" + opus)
        data = [rank, name, opus, version, duration, author_name, author_life]
        music_data.append(data)
    # 曲目数量不满20的继续读页面右边一列
    if i != 19:
        curr_rank = i
        i = 0
        for temp in range(curr_rank, 20):
            # 曲名
            name_path = '//*[@id="div2"]/table/tbody/tr[{}]/td[1]/a/text()'.format(i + 2)
            # 作品数不满20
            if not selector.xpath(name_path):
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


def write_data_to_csv(columns, datas):  # 将数据写入csv
    test = pd.DataFrame(columns=columns, data=datas)  # 将数据放进表格
    test.to_csv('music_data_new2.csv')  # 数据存入csv,存储位置及文件名称


if __name__ == '__main__':
    path = 'musicians_relationships_eng.csv'  # 关系csv文件路径
    composer_list = read_csv(path)
    for composer in composer_list:
        get_urls(composer)
    get_info('https://www.classiccat.net/beethoven_l_van/index.php')
    print("开始写入csv。。。")
    header = ['rank', 'name', 'opus', 'versions', 'duration', 'composer_name', 'composer_life']
    write_data_to_csv(header, music_data)
    print("End....")