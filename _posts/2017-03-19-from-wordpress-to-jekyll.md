---
layout: post
title:  "我为什么放弃WordPress而选用Jekyll + Github Pages?"
date:   2017-03-19 17:00:00 +0800
categories: blogging
tags: 
 - blogging
 - WordPress
 - Jekyll
---

## 为什么放弃用了十年的WordPress?

大约在2007年, 我第一次把WordPress安装在了一个共享的虚拟主机上. 边用边学, 一用就是10年. 自己配置,维护一个独立WordPress让我学到一些技术: 略懂了一点PHP, MySQL, 写过一个WordPress插件, 还为了备份而写过一个Python Package.
 
### 当初为什么要安装独立的WordPress?
 
 多数的博客服务提供商都会有所限制, 而我想要足够灵活的控制, 所以只能自己安装.  WordPress满足了我的需要, 并且: 
 - 容易安装, PHP + MySQL就足够 
 - 插件丰富, 扩展功能简单
 - 可以顺便学习PHP, MySQL, 文档内容丰富.
 
### 为什么要放弃WordPress?

我遇到的痛点 + 解决方案:
 - 垃圾评论: 安装反垃圾插件 -> 停用评论 -> 改用DISQUS
 - 备份:  压缩(dump database + 网站目录)-> 上传到Dropbox备份. 自己写了个[Python工具](http://liguoliang.com/side-projects/rabbit-backup/)来上传备份, 上传完毕后再下载验证, 然后删除本地及Dropbox上的旧备份. 
 
这其实是每个独立博客都会面临的问题. 

## 简洁稳定的新选择:  Jekyll + Github Pages

吸引我的是简单. 

我不再是那个校园里的少年, 彼时追求的一些东西, 现在可能已经淡忘. 所以我需要的一个服务, 一个既能稳定, 还能还给我自由的服务. 
 - Github Pages 提供build + 网页存储服务 
 - Jekyll 提供我简单与自由的写作体验

我没有任何Ruby经验, 也不熟悉安装各类包. 用Vagrant写了一个快速搭建Jekyll开发环境的脚本: [jekyll-vagrant](https://github.com/guoliang-dev/jekyll-vagrant)
 - 启动一个Ubuntu 14
 - 设置port forwarding
 - 安装Ruby,Jekyll
 
 `vagrant up`之后就可以用Jekyll跑本地的网站了 

### 迁移过程
 - WordPress迁移到子域名;
 - 主域名交给Cloudflare管理, 并使用其CDN, Flexible SSL服务
 - 主域名转向到Github
 - 必要的http 301转向, 保证旧的文章还能被访问. 
 
