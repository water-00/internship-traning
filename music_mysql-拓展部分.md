# music_mysql说明文档——拓展部分

## 系统简介

⼀个简单的个⼈⾳乐收藏数据库，有查询⾳乐、查询作曲家、添加⾳乐、删除⾳乐等功能。

## 拓展功能描述

### 1.数据来源

通过网络爬虫，得到真实大量的古典音乐信息。

如每首曲子的rank,name,opus,versions,duration,composer_name,composer_life等信息。

再通过数据处理，如分词等操作，得到我们需要的与关系型数据库匹配的数据。

在关系型数据库中，我们创建了piece和composer两种表，有爬虫的到的信息进行切割，得到相对应的数据。

### 2.可视化程序

使用python的tkinter可视化工具，实现了乐曲查询程序的可视化，同时通过Pyinstaller库将程序打包封装为exe可执行文件以方便移植。

### 3.多表查询

通过多表查询，将piece与composer连接，获取一首乐曲的全部信息。

**查询语句**：select opus opus, piece.name name, piece.composer composer, piece.album album, composer.birthplace birthplace from piece, composer where piece.composer = composer.name;

### 4.完善功能

新增加了添加专辑、添加作曲家信息的界面与功能。
