---
layout: post
title:  "Lessons Learned from Take-Home-Projects in Job Interviews"
date:  20190829 12:40:18 +0800
categories: default 
tags:
 - lessons-learned
 - job-interview
 - take-home-project
---

Consider a take-home-project an opportunity to demonstrate your design and coding skills. writing a`Factory` to produce intances is much more interesting than answering 'can you tell me one design pattern that you used?'

## Prepare a seed/template project to save time

e.g. https://github.com/guoliang-dev/java8-maven-seed-project:
 - a default pom.xml with dependencies(e.g. junit) and plugins(e.g. jaccoco)
 - a default CI config e.g. bitbucket
 - a default readme


## Put your solution into a remote *private* repo and setup build pipeline

such as github/bitbuket, make sure it's a *private* one and build pipeline is enabled. both github and bitbuket are offering certain free minutes for *private* repo build.


## Prepare a readme.md

typically a readme file should contains:
 - your name, email and your github url
 - assumptions
 - high level design
 - TODO items: show that you can continue ehancing the project if you got more time

 however, don't expect that interviewers will read all details carefully. 


## Add comments in your code

this will help interviewers understand your code and also let them know that you're aware of poetnial issues. 

generally I'll try my best on naming, so that I dont need to add comments. howerver, comments will help for:
 - complex codes
 - messy codes, e.g: // todo: refactoring required, should reduce the size of this method
 - shortcut. e.g: // todo: use proper ThreadPool to handle MT


## Unit tests / intergration tests / end-to-end tests

**always** write unit tests, even though it's not mentioned at all, ideally follow `TDD`.
 - tests help you verify your solution
 - tests help you make further changes safely
 - tests help you design your project in clean way


## Think about the next stpes

you may required to have code review sessions with interviewers:
 - you need to share your design and might get challenged about the technical design you made
 - you might required to fix certain bugs or add features


## Coding during interview

if you're requested to fix a bug or add an enhancement, make sure:
 - run all your tests before making any change
 - limit your change scope: only make minimal necessary changes to delievery the task, you might want to refactor a lot *DO NOT* change anything if it's not linked to the task.
