---
layout: post
title:  "My thoughts on Python vs Java"
date:  20220409 23:30:00 +0800
categories: default
tags:
 - Python
 - Java
---

After working in both Python and Java for a while, I want to share my thoughts on the two languages.


## Popularity

My current project has a REST API to let users query prices data,  our users are mostly big corporations, such as energy companies, financial institutions.
To help users getting started with the API, we also provide few code samples, in both Python (our primary language) and Java. 
We added Java because we think it's more popular in big companies.

In the last 2 years, we received many questions about the code sample in Python, but 0 question about the Java sample.
why? one reason cloud be the Java sample is perfect and everybody understands it well. but after checking the users email signatures,
I found that most of the users are not developers, they're analysts, traders,  they just want to copy some simple code and run it.

in terms of popularity in non-developers, for sure Python is the much more popular, IMO:
 - if I'm going to start a new project which involves business users, probably I should start with Python.
 - if I need to release an SDK related to data, I probably should start with Python.


## Delivery Speed

If I need to build some PoC projects quickly, I'll start with a python script. yes, just a script. why bother with a Java project?
The language is simple and easy to communicate with other non-technical users, and most importantly, there are so many open source libraries and modules available.


## Bigger projects? more developers?

What happen if the PoC script went well?  project getting bigger, more developer joining? we need to be split the
big project to smaller modules (but not small projects yet to save the time to release the internal packages).  what happen if I want to have a `common` module?
currently, we're using ["Poetry"](https://python-poetry.org/docs/dependency-specification/#path-dependencies):
> To depend on a library located in a local directory or file, you can use the path property:
> my-package = { path = "../my-package/", develop = false }

This works for simple projects,  but for a project with different module structures, some workarounds are needed, such as creating a symbolic link.
but in Java side,  "Maven" supports this perfectly.

with more developers onboard, more runtime exceptions may happen due to the nature of dynamic language, Java is a much
safer language to use.  the compiler reduces many runtime errors that cloud happen in Python.

In short, Java is more enterprise-ready than Python, but I believe python is catching up.


## Ecosystem, supply chain

"Spring" is the most popular Java framework, backed by a listed company. it almost has everything, for some java developers, they can't survive without Spring.
However, in python side, libraries are less commercialized, which means you may need to raise a pull request to fix your own issue.  


