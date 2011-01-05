#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8
"""
fetch_xmls.py
"""

#import os
#import re
#import shutil
import urllib

kytargetdir = '/home/msworks/www/kyxml'
kyurlprefix = 'http://vid.mandsworks.com/ky/'

xmls = [
#    ('xmlsource','targetpath','outfile'),
    (kyurlprefix+'how/byFolderOrder.xml',kytargetdir,'how2play.xml'),
    (kyurlprefix+'news/byFolderOrder.xml',kytargetdir,'news.xml'),
    (kyurlprefix+'od/byShowDate.xml',kytargetdir,'recent.xml'),
    ]


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
            print "got %s%s" % (xmlsrc,targetpath)


def main():
    createfiles(xmls)


if __name__ == '__main__':
    main()
