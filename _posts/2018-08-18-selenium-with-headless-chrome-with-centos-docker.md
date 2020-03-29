---
layout: post
title:  "Run Selenium with Headless Chrome in Docker(CentOS)"
date:  20180818 17:10:35 +0800
categories: default 
tags:
 - selenium
 - headless-chrome
 - docker 
---

As an engineer, I want to test my web app with Chrome in a Jenkins cluster. Chrome is not available in most of 
Jenkins build nodes, but docker is.

## build image

based on `CentOS`, install headless chrome, selenium and chromedriver.

```
FROM centos:7

LABEL org.label-schema.schema-version="1.0" \
    org.label-schema.name="Selenium with Headless Chrome and CentOS" \
    org.label-schema.vendor="liguoliang.com" \
    org.label-schema.license="GPLv2" \
    org.label-schema.build-date="20180817"

# install necessary tools
RUN yum install unzip -y
RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

# install headless chrome
RUN curl -O  https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
RUN yum install google-chrome-stable_current_x86_64.rpm -y

# install selenium
RUN pip install selenium

# download chromedriver
RUN mkdir /opt/chrome
RUN curl -O https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip -d /opt/chrome

# copy the testing python script
COPY selenium-with-headless-chrome.py .
RUN python selenium-with-headless-chrome.py
```

## execute selenium from python

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(r'/opt/chrome/chromedriver', chrome_options=chrome_options)

driver.get("http://python.org")
print "page title: %s" % driver.title
```

## docker image & source code

* docker image: https://hub.docker.com/r/guoliangli/selenium-with-headless-chrome-centos/ 
* source: https://github.com/guoliang-dev/docker-selenium-with-headless-chrome-centos


## troubleshootings

### Public key for google-chrome-unstable-x.rpm is not installed

solution: import google key e.g.
```
rpm --import https://dl-ssl.google.com/linux/linux_signing_key.pub
```
for more detials: https://www.google.com/linuxrepositories/

### ERROR Message: unknown error: DevToolsActivePort file doesn't exist

add arguments: 
```
 "--headless",
 "--no-sandbox",
 "--disable-dev-shm-usage"
```
for more details: 
* https://github.com/timgrossmann/InstaPy/issues/2362
* https://github.com/karma-runner/karma-chrome-launcher/issues/158
