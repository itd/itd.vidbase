#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8
"""
inotify_published_file_handler.py
----

Created by Kurt Bendl


Usage
---------
sudo su - www-data -c 'cd /web/log/; \
  nohup /web/scripts/inotify_published_file_handler.py > \
  /web/log/inotify-errors.txt 2>&1  &'


Purpose
---------
Monitor the $WEBROOT/aapracing/import/publish directory.
Once a file is closed, act on it:

1. Copy the PDF and XML files from source_dir to vtarget_dir
2. If the file is an.XML, copy it to the xml_ftp_dir
3. Make the dummy file for PHP publishing process
4. Maze a .zip version of the file
5. Remove the source file

Requirements
------------
 * Linux kernel 2.6.13 +
 * pyinotify 2.8.6 +


Installation
--------------
To install pyinotify on ubuntu/debian:

1. install distribute:
     curl -O http://python-distribute.org/distribute_setup.py
     sudo python distribute_setup.py
2, Get the latest pyinotify lib from:
    http://seb.dbzteam.org/pub/pyinotify/releases/
    curl -O http://seb.dbzteam.org/pub/pyinotify/releases/pyinotify-0.8.9.tar.gz
    sudo easy_install pyinotify-0.8.9.tar.gz


Docs
-----
Docs on pyinotify can be found here: http://trac.dbzteam.org/pyinotify/wiki

"""

import os
import re
import shutil
import pyinotify
import datetime
import zipfile
import time
from ..config import ITDVIDEO_STORAGE_PATH as source_dir

### production config info
#source_dir =      "/web/ausracing.mighty-site.com/aapracing/publish/data/publish/"
vtarget_dir = "/web/ausracing.mighty-site.com/filebin/downloads/"
reference_path =  '/web/ausracing.mighty-site.com/aapracing/publish/data/published/'
xml_ftp_dir =     "/home/ftp/private/xml/"
filez =           '(mp4|m4v|txt)'
logfile_path =    "/web/log/inotify.log"
woodbine_xml_dir = "/home/ftp/woodbine/xml/"
woodbine_xml_zips =     "/home/ftp/woodbinexml/"

testing = 'false'
if testing == 'true':
#  source_dir =      "/web/wyvern/tmp/src/"
  vtarget_dir = "/web/wyvern/tmp/file/"
  reference_path =  '/web/wyvern/tmp/ref/'
  xml_ftp_dir =     "/web/wyv ern/tmp/xml/"
  logfile_path =    "/web/wyvern/tmp/inotify.log"
  woodbine_xml_dir = "/web/wyvern/tmp/woodbinexml/"
  woodbine_xml_zips =     "/web/wyvern/tmp/woodbineftp/"



def getNow():
  """Just return the current time for timestamping logs"""
  return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def makeReferenceFile(tfile):
  open(tfile, 'w').close()


class SourceMonitor(pyinotify.ProcessEvent):
  """ Watches the source dir for IN_CLOSE_WRITE event"""

  def process_IN_CLOSE_WRITE(self, event):
    """when an IN_CLOSE_WRITE happens, do stuff"""
    time.sleep(4)
    if re.search('(.*\.'+filez+'$)', event.pathname):
      # We have a match, put a copy into the filebin dir
      shutil.copy2(event.pathname, vtarget_dir)
      time.sleep(1)
      logfile = open(logfile_path, "a")
      logfile.write("%s: %s copied to: %s \n" %
                    (getNow(), event.pathname, vtarget_dir)
                    )

      if re.search('(.*\.(XML|xml)$)', event.pathname):
        # If it's and XML, put a copy in the FTP dir
        time.sleep(1)
        shutil.copy2(event.pathname, xml_ftp_dir)
        time.sleep(1)
        logfile.write("%s: %s copied to: %s \n" %
                      (getNow(), event.pathname, xml_ftp_dir)
                      )

      #woodbine specific copy
      if event.pathname.endswith(('AUS_AUS.XML','AUB_AUS.XML')):
        # If it's AUB or AUS, put a copy in woodbine_xml_dir
        time.sleep(1)
        shutil.copy(event.pathname, woodbine_xml_dir)
        time.sleep(1)
        logfile.write("%s: %s copied to: %s \n" % (getNow(), event.pathname, woodbine_xml_dir))

      # Make zipe files for philly and woodbine
      makeZipFile(event.pathname, xml_ftp_dir)
      time.sleep(1)
      makeZipFile(event.pathname, woodbine_xml_zips)

      # Make the dummy file marker to enable PHP
      # to know the file is really published
      fhandle = os.path.basename(event.pathname)
      open(reference_path + fhandle, 'w').close()

      # Now, whack the source file since we're done with it.
      os.remove(event.pathname)
      logfile.write("%s: %s removed. \n" % (getNow(), event.pathname))


event_mask = pyinotify.IN_CLOSE_WRITE
wm = pyinotify.WatchManager()
p = SourceMonitor()
notifier = pyinotify.Notifier(wm, p)
#wm.add_watch(source_dir, event_mask)
wdd = wm.add_watch(source_dir, event_mask)

print "This should have been started with:\n"
print "  sudo su - www-data -c 'cd /web/log/; \\"
print "  nohup /web/scripts/inotify_published_file_handler.py > \\"
print "  /web/log/inotify-errors.txt 2>&1  &' \n\n"

notifier.loop()

