import datetime
import sys
import re

now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')
timestamp = now.strftime('%Y%m%d %H:%M:%S')
title = sys.argv[1] if len(sys.argv) > 1 else 'post' 
slug=re.sub("[-]+", "-", re.sub("[^a-zA-Z0-9]", "-", title)).lower()
path = '_posts/%s-%s.md' % (today, slug) 

print 'path: %s' % path

header = """ 
---
layout: post
title:  "%s"
date:  %s +0800
categories: default 
tags:
---
""" % (title, timestamp)

print header

with open(path, "w+") as f:
    f.write(header)

if len(sys.argv) == 1:
    print '***WARN: default title is used***'
