#!/usr/bin/env python3  
# -*- coding: utf-8 -*-
import urllib.request
from datetime import datetime
import traceback
import socket
from bs4 import BeautifulSoup
import os
#re模块主要包含了正则表达式
import re
#定义一个getHtml()函数
imgPath='E:/private/caoliuimage/girl/'
#http://www.xianqiinsh.com/thread0806.php?fid=8&search=&page=2
#http://www.xianqiinsh.com/thread0806.php?fid=8&search=&page=3

downUrl='http://www.xianqiinsh.com/thread0806.php?fid=8&search=&page='

def getHtmlByUrl(url):
    try:
        page = urllib.request.urlopen(url)  #urllib.urlopen()方法用于打开一个URL地址
        html = page.read() #read()方法用于读取URL上的数据
        htmlStr = str(html)
#         print(htmlStr)
        return htmlStr 
    except Exception as e:
        print("获取页面html失败:"+url)
        print('请求失败:%s' % e)
        traceback.print_exc()
def getDirNameByHerfValue(url,herfUrl):
    try:
        page = urllib.request.urlopen(url)  #urllib.urlopen()方法用于打开一个URL地址
        html = page.read() #read()方法用于读取URL上的数据
#         print(html.decode('gbk'))
        htmlSoup = BeautifulSoup(html,'html.parser')
        dirname = htmlSoup.find_all(href=herfUrl)[1].get_text()
        print("获取到的dirname:"+dirname)
        return dirname
    except Exception as e:
        print('请求失败:%s' % e)
        print("获取dirname失败:"+herfUrl)        
        traceback.print_exc()
def getAllImgUrlByUrl(url):
    try:
        print("-------获取所有图片url:%s" %  url)
        html = getHtmlByUrl(url)
        reg = r'src="(https?://.+?/.+?/.+?\..+?g)"'    #正则表达式，得到图片地址
        imgre = re.compile(reg)     #re.compile() 可以把正则表达式编译成一个正则表达式对象.
    #     print(type(html))
        imgUrllist = re.findall(imgre,html)      #re.findall() 方法读取html 中包含 imgre（正则表达式）的    数据
        #去重
        imgUrllist=list(set(imgUrllist))
        print("获取到的图片url size(去重之后):"+str(len(imgUrllist)))
        for imgUrl in imgUrllist:
            print(imgUrl)
        return imgUrllist
    except Exception as e:
        print('请求失败:%s' % e)
        print("获取全部图片地址失败:"+url)
        traceback.print_exc()
        
def getAllPageUrlByUrl(url):
    try:
        print("-------获取所有page url:%s" %  url)
        html = getHtmlByUrl(url)
#         reg = r'href="(https://www\.zhihu\.com/question/.+?/answer/.+?)"'    #正则表达式，得到图片地址
        reg = r'href="(cl552/8/1611/.+?\.html)"'    #正则表达式，得到图片地址
        imgre = re.compile(reg)     #re.compile() 可以把正则表达式编译成一个正则表达式对象.
    #     print(type(html))
        pageUrllist = re.findall(imgre,html)      #re.findall() 方法读取html 中包含 imgre（正则表达式）的    数据
        pageUrllist=list(set(pageUrllist))
        print("获取到的pageurl size(去重后):"+str(len(pageUrllist)))
        for imgUrl in pageUrllist:
            print(imgUrl)
        return pageUrllist
    except Exception as e:
        print('请求失败:%s' % e)
        print("获取全部page地址失败:"+url)
        traceback.print_exc()
        
def getAllSinglePageImgByUrl(pageurl,dirname):
    imglist = getAllImgUrlByUrl(pageurl)
    #把筛选的图片地址通过for循环遍历并保存到本地
    #核心是urllib.urlretrieve()方法,直接将远程数据下载到本地，图片通过x依次递增命名
    for imgurl in imglist:
        try:
            print("正在下载图片:"+imgurl)
            urllib.request.urlretrieve(imgurl,imgPath+dirname+"/"+datetime.now().strftime('%Y%m%d%H%M%S%f')+os.path.splitext(imgurl)[1])
#             urllib.request.urlretrieve(imgurl,imgPath+datetime.now().strftime('%Y%m%d%H%M%S%f')+os.path.splitext(imgurl)[1])
            print("下载完成...")
        except Exception as e:
            print('请求失败:%s' % e)
            print("下载图片失败:"+imgurl)
            traceback.print_exc()
def getAllImage(url):
    pageUrlList = getAllPageUrlByUrl(url)
    for pageurl in pageUrlList:
        try:
            #get the dir name
            dirname = getDirNameByHerfValue(url,pageurl)
            print("新建子目录名称:"+imgPath+dirname)
            if os.path.exists(imgPath+dirname) != True: #目录不存在就创建
                os.makedirs(imgPath+dirname)
            getAllSinglePageImgByUrl("http://www.xianqiinsh.com/"+pageurl,dirname)
        except Exception as e:
            print('请求失败:%s' % e)
            print("获取单页所有图片失败:"+pageurl)
            traceback.print_exc()
if __name__=='__main__':
    socket.setdefaulttimeout(5)
    for i in range(1,293):
        print("------------开始下载第%s页的图片--------------" % (str(i)))
        getAllImage(downUrl+str(i))
    print("下载完成.....")