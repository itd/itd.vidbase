#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
"""
fetch_xmls.py
"""

#import os
#import re
#import shutil
import time
import datetime
import urllib

kytargetdir = '/home/msworks/www/kyxml/'
kydtargetdir = '/home/msworks/gooch/'
kyurlprefix = 'http://vid.mandsworks.com/ky/'

xmls = [
#    ('xmlsource','targetpath','outfile'),
    (kyurlprefix+'how/byFolderOrder.xml',kytargetdir,'how2play.xml'),
    (kyurlprefix+'news/byFolderOrder.xml',kytargetdir,'news.xml'),
    (kyurlprefix+'od/byShowDate.xml',kytargetdir,'recent.xml'),
    (kyurlprefix+'desktop-news/byShowDate.xml',kytargetdir,'desk_news.xml'),
    ]

def getNow():
  """Just return the current time for timestamping logs"""
  return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def fetchxmldata(xmlsrc):
    """"""
    sock = urllib.urlopen(xmlsrc)
    data = sock.read()
    sock.close()
    return data


def createfiles(xmls):
    """"""
    for item in xmls:
        xmlsrc =     item[0]
        targetpath = item[1]
        outfile =    item[2]
        data = fetchxmldata(xmlsrc)
        if data.startswith('<rss'):
            f = open(targetpath+outfile,'w')
            f.write(data)
            f.close()
            print "%s; got %s" % (getNow(), outfile)


def main():
    while 1 == 1:
        createfiles(xmls)
        time.sleep(90)


if __name__ == '__main__':
    main()