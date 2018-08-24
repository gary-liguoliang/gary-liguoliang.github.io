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

mutiple JDK can be installed: e.g. java 1.8 and java 10.


## check installed jdk
run `man java_home` to know how:

> The  java_home  command  returns a path suitable for setting the JAVA_HOME environment variable.  It determines this path
       from the user's enabled and preferred JVMs in the Java Preferences application.  Additional constraints may  be  provided
       to  filter the list of JVMs available.  By default, if no constraints match the available list of JVMs, the default order
       is used.  The path is printed to standard output.

```bash
bash-3.2$ /usr/libexec/java_home -V
Matching Java Virtual Machines (2):
    10.0.2, x86_64:	"Java SE 10.0.2"	/Library/Java/JavaVirtualMachines/jdk-10.0.2.jdk/Contents/Home
    1.8.0_45, x86_64:	"Java SE 8"	/Library/Java/JavaVirtualMachines/jdk1.8.0_45.jdk/Contents/Home


bash-3.2$ /usr/libexec/java_home -v 1.8 --exec java -version
java version "1.8.0_45"
Java(TM) SE Runtime Environment (build 1.8.0_45-b14)
Java HotSpot(TM) 64-Bit Server VM (build 25.45-b02, mixed mode)

bash-3.2$ /usr/libexec/java_home -v 10 --exec jshell
|  Welcome to JShell -- Version 10.0.2
|  For an introduction type: /help intro

jshell> /exit
|  Goodbye


bash-3.2$ export JAVA_HOME=`/usr/libexec/java_home -v 1.8`
bash-3.2$ java -version
java version "1.8.0_45"
Java(TM) SE Runtime Environment (build 1.8.0_45-b14)
Java HotSpot(TM) 64-Bit Server VM (build 25.45-b02, mixed mode)
```

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
