#!/bin/sh
SERVICE='inotify_published_file_handler.py'

if ps ax | grep -v grep | grep $SERVICE > /dev/null
then
    echo "$SERVICE service running, everything is fine"
else
    #echo "$SERVICE is not running"
    su - www-data -c 'cd /web/log/; nohup /web/scripts/inotify_published_file_handler.py > /web/log/inotify-errors.txt 2>&1  &'
fi
