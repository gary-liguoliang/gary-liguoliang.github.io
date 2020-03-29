import datetime
import sys


now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')
timestamp = now.strftime('%Y%m%d %H:%M:%S')
short_title = sys.argv[1] if len(sys.argv) > 1 else 'post' 
path = '_posts/%s-%s.md' % (today, short_title) 

print 'path: %s' % path

header = """ 
---
layout: post
title:  "%s"
date:  %s +0800
categories: default 
tags:
 - blogging
---
""" % (short_title, timestamp)

print header

with open(path, "w+") as f:
    f.write(header)

if len(sys.argv) == 1:
    print '***WARN: default title is used***'
