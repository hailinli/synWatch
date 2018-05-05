#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'lihailin'  
__mail__ = '415787837@qq.com'  
__date__ = '2018-05-03'  
__version__ = 1.0 

import sys
import time
import ftp
# 配置日志
import logging
import log
log.initLogConf()
_logging = logging.getLogger(__file__)
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
reload(sys)
sys.setdefaultencoding('utf-8')


# 配置ftp
ip = '58.87.123.159'
username = 'ubuntu' 
passwd = '19911882lhl' 

class ToServer(FileSystemEventHandler):
    '''
    将本地文件变化事件记录到日志中，并上传到服务器
    '''
    def on_any_event(self, event):
        # 将发生过的事件写入日志
        if event.is_directory:
            is_d = 'directory'
        else:
            is_d = 'file'
        log_s = "%s %s: %s " % (event.event_type, is_d, event.src_path)
        # print log_s
        _logging.info(log_s)

    def on_created(self, event):  
        # 仅上传文件
        if event.is_directory:
            return  
        xfer.upload(event.src_path)
        log_s = "upload file: %s " % event.src_path
        _logging.info(log_s)
        

    def on_modified(self, event):  
        self.on_created(event)


    def on_moved(self, event):
        '''
        服务器中的文件进行移动
        '''
        xfer.rename(event.src_path, event.dest_path)
        log_s = "move file: %s to %s" % (event.src_path, event.dest_path) 
        _logging.info(log_s)


if __name__ == "__main__":
    # 配置ftp服务器
    xfer = ftp.Xfer()  
    xfer.setFtpParams(ip, username, passwd)

    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    # 开启服务时上传一遍文件至远程文件夹
    xfer.upload(path)
     
    event_handler = ToServer()  
    observer = Observer()  
    observer.schedule(event_handler, path, recursive=True)  
    observer.start()  
    try:  
        while True:  
           time.sleep(1)
    except KeyboardInterrupt:  
        observer.stop()  
    observer.join()  
