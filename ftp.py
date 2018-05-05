#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'lihailin'  
__mail__ = '415787837@qq.com'  
__date__ = '2018-05-03'  
__version__ = 1.0  
  
import sys  
import os  
from ftplib import FTP  
import logging
import log
log.initLogConf()
_logging = logging.getLogger(__file__)
reload(sys)
sys.setdefaultencoding('utf-8')
  
  
import socket  
timeout = 1000    
socket.setdefaulttimeout(timeout)

class Xfer(object):  
    ''''' 
    上传本地文件或目录递归上传到FTP服务器 
    '''  
    def __init__(self):  
        self.ftp = None  
      

    def setFtpParams(self, ip, uname, pwd, port = 21, timeout = 60):  
        # 设置ftp参数        
        self.ip = ip  
        self.uname = uname  
        self.pwd = pwd  
        self.port = port  
        self.timeout = timeout  
      

    def initEnv(self):  
        # 链接ftp
        if self.ftp is None:  
            self.ftp = FTP()  
            _logging.debug('### connect ftp server: %s ...'%self.ip) 
            self.ftp.connect(self.ip, self.port, self.timeout)  
            self.ftp.login(self.uname, self.pwd)   
            _logging.debug(self.ftp.getwelcome())
      

    def clearEnv(self):  
        # ftp断开链接
        if self.ftp:  
            self.ftp.close()  
            # self.ftp.quit(), close和quit只能选一个
            _logging.debug('### disconnect ftp server: %s!'%self.ip)  
            self.ftp = None  
    

    def uploadFile(self, localpath, remotepath='./'): 
        ''' 
        上传文件至服务端，为了保存本地和服务器路径一致
        loacalpath路径文件夹需是单层，如'a/b/c.txt'是不行的。
        '''
        if not os.path.isfile(localpath):    
            return  
        _logging.info('+++ uploading %s to %s:%s'%(localpath, self.ip, remotepath))
        try:
            self.ftp.storbinary('STOR ' + remotepath, open(localpath, 'rb'))
            _logging.info('upload success: %s '%localpath)  
        except Exception as e:
            _logging.info('upload fail %s : %s'%(localpath, e))


    def uploadDir(self, localdir='./', remotedir='./'):  
        '''
        localdir 里面的文件以及全部同步到服务器的remotedir
        为了保存本地和服务器路径一致，localdir路径需是单层，如'a/b/c'是不行的
        '''
        # print sdfsdf 为了产生bug方便测试

        if not os.path.isdir(localdir):    
            return  
        self.ftp.cwd(remotedir)
        for file in os.listdir(localdir):  
            src = os.path.join(localdir, file)  
            if os.path.isfile(src):
                self.uploadFile(src, file)  
            elif os.path.isdir(src):  
                try:    
                    self.ftp.mkd(file)    
                except:    
                    # sys.stderr.write('the dir is exists %s'%file)  
                    # _logging.error('the dir is exists %s'%file)
                    pass
                self.uploadDir(src, file)  
        self.ftp.cwd('..')  

      
    def walkLastServer(self, src):
        '''
        在服务端递归创建文件夹，如'a/b/c'
        并将cd到最里层文件夹
        '''
        deldictorys = src.split('/')
        for d in deldictorys[:-1]:
            try:    
                self.ftp.mkd(d)    
            except:
                pass    
            self.ftp.cwd(d)
        return deldictorys[-1]
      

    def _upload(self, src):  
        '''
        可同时上传文件以及文件夹
        文件夹及文件路径可含有多层，'desk/za/a.txt'是可行的
        '''
        self.initEnv() 
        desSrc = self.walkLastServer(src)
        if os.path.isdir(desSrc):  
            try:    
                self.ftp.mkd(src)    
            except:
                pass
            try:
                log_s = "+++ uploading directory %s" % desSrc 
                _logging.info(log_s)
                self.uploadDir(desSrc, desSrc)
                log_s = "upload directory sucess: %s" % desSrc 
                _logging.info(log_s)  
            except Exception as e:
                _logging.error(e)
                log_s = "upload directory fail: %s" % desSrc 
                _logging.info(log_s)  
        elif os.path.isfile(src):  
            self.uploadFile(src, desSrc)
        self.clearEnv()    
    

    def upload(self, src, times=3):
        '''
        上传文件是一个耗时的操作，防止timeout
        '''
        try:
            self._upload(src)
        except Exception as e:
            _logging.error(e)
            times -= 1
            if times>0:
                _logging.info('======重传文件: %s ======' % src)
                self.upload(src,times)


    def rename(self, fromname, toname):
        self.initEnv() 
        logging.info('+++ rename %s to %s'%(fromname, toname))
        try:
            self.ftp.rename(fromname, toname)
            logging.info('rename success: %s' %fromname)
        except Exception as e:
            _logging.error(e)
            logging.info('rename fail %s : %s' %(fromname, e))

        self.clearEnv()   


    # def delFile(self, remotefile):
    #     '''
    #     删除文件，路径可是多层
    #     '''
    #     if not os.path.isfile(remotefile):    
    #         return
    #     self.initEnv() 
    #     self.ftp.delete(remotefile)
    #     self.clearEnv()


    # def delDictory(self, remotedic):
    #     '''
    #     删除文件夹，路径可是多层
    #     '''
    #     self.initEnv() 
    #     for a,b,c in os.walk(remotedic,topdown=False):
    #         for ai in a:
    #             for ci in c:
    #                 self.delfile(os.path.join(ai, ci))
    #             self.ftp.rmd(ai)
    #     self.clearEnv()


if __name__ == '__main__':  
    
    ip = 'xxxx.xxxx.xxxx.xxxx'
    username = 'xxxx' 
    passwd = 'xxx'
    
    # to = 'offer/tencent-实习offer'
    # src = 'offer/相关资料/tencent-实习offer'
    # xfer = Xfer()  
    # xfer.setFtpParams(ip, username, passwd)     
    # xfer.rename(src, to)

    # #测试
    # srcFile = r'offer'
    # srcFile = 'offer/相关资料/成绩单.docx'
    # xfer = Xfer()  
    # xfer.setFtpParams(ip, username, passwd)    
    # xfer.upload(srcFile) 