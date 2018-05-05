毕业在即，闲着无聊，偶然发现腾讯云主机正在搞活动，于是买了一台云主机。想用跑一些日常小任务，如爬虫。然而在云主机上利用vim进行程序开发实在麻烦，本地开发完程序还需手动同步到服务端，太过麻烦。
[搭建samba](https://blog.csdn.net/linhai1028/article/details/80200256)后发现mac访问腾讯云主机上的samba速度很慢，ftp速度还是比较快的。因此就想着自己写一个自动同步本地代码到云主机的python脚本。

-----

## 一、搭建ftp服务器
搭建ftp服务器见文章[ubuntu16.04搭建ftp服务器](https://blog.csdn.net/linhai1028/article/details/80197254)

## 二、思路简介
本文工具主要利用watchdog对文件夹做监听，如发现文件夹中的文件有移动、创建、重命名、修改操作，那么就把对应的修改上传到ftp服务器。如文件夹某文件删除了，那么不对服务端的数据做处理。也就是对ftp服务器的数据做增量更新。

## 三、模块简介
### 1. 日志处理模块
日志处理模块主要是设置日志格式，日志输出等，其代码对应于文log.py
### 2. ftp模块
主要是基于ftplib库，利用python代码实现文件从ftp服务器上传、下载、删除、移动等，主要代码ftp.py
### 3. watchdog监听模块
利用watchdog对文件夹做监听，如发现文件夹中的文件有移动、创建
、重命名、修改操作，那么就把对应的修改上传到ftp服务器。如文件夹某文件删除了，那么不对服务端的数据做处理。

## 四、使用

### 1. [下载项目代码](https://github.com/hailinli/synWatch/archive/7080c7d58b7852927caa448dfef0bc41e38dfe38.zip)
修改synWatch.py中的配置信息，配置信息有ftp服务器的ip地址，ftp用户名、密码。

```
 ip = 'x.x.x.x'
 username = 'xxxx'
 passwd = 'xxxx'
```
### 2. 进行文件监听
```
# yourpath为你要监听的本地目录
python synWatch.py yourpath
```

------

## 环境
1. MacOS X 10.11.6
2. python2.7
3. watchdog 0.83 



