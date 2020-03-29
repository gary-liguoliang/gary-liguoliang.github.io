---
layout: post
title:  "Time Series Analysis with Python"
date:  20190719 23:32:44 +0800
categories: default 
tags:
 - python 
---

I have a log file contains numbers indexed in time, I want to generate time series chart to display the data to my users. 
However I'm new to data visualization, so I'm tracking what I did in this post.

## Environment Setup
Jupyter is a nice tool to playaround with python, so get it installed or get a docker instance:
```
docker run --rm -p 8888:8888 -v "$PWD":/Users/gouliang/jupyter-home jupyter/scipy-notebook
```

if you're not sure about which image to choose: https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html

url with access token will be displayed on the console. 

## Hello world
start a python notebook and run:
```
## https://stackoverflow.com/questions/19079143/how-to-plot-time-series-in-python

import matplotlib.pyplot as plt
import datetime
import numpy as np

x = np.array([datetime.datetime(2013, 9, 28, i, 0) for i in range(24)])
y = np.random.randint(100, size=x.shape)

plt.plot(x,y)
plt.show()
```
a nice time series chart will be displayed.

#WIP
