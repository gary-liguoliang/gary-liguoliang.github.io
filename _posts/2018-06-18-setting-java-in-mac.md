---
layout: post
title:  "Installing and configuring Java/Maven environment in Mac"
date:  2018-06-18 23:00:00 +0800
categories: dev
tags:
 - java
 - maven
 - mac
---

## installing jdk

download and install jdk from: 
http://www.oracle.com/technetwork/java/javase/downloads/index.html

## configuring java_home

according to `man java_home`:
set java_home in `~/.bash_profile`:
```bash
export JAVA_HOME=`/usr/libexec/java_home`
```

## installing / configuring maven

download and unzip maven, then set m2_home in `~/.bash_profile`:
```
export M2_HOME=$tools/current-maven
export PATH=$M2_HOME/bin:$PATH
```

**check maven settup**

`mvn -v` will print the maven home and java home.  if java home is incorrect, verify your environment details with your `$M2_HOME/bin/mvn`.
