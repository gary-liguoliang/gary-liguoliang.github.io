---
layout: post
title:  "How does poor application change my career path in the last few years"
date:  20190710 21:43:47 +0800
categories: default
tags:
 - QA
 - DevOps
 - Dev
---

> I have been working as a developer since 2007, most of my time is spent on certain products. however in the last 3 years, I spent most of my time on QA automation and DevOps. this post is the reason behind my switch.


it was 2015, I was working at an American multinational investment bank, as an application developer.
one of the applications is a file mover which moves file from one location to another, such as pulling files from one folder in ServerA and put them to another folder in ServerB.

the file mover has been heavily used in few markets for few years, it's a internal built app, so we have all the source codes with very limited unit tests.

my task was to add support to SFTP so that the file mover can pull files from remote severs via SFTP.

it looks very simple and well-defined, so I just added my code (and tried not to touch anything else) with unit tests and managed to get approved to production.

Production issue happened after my release, I was told that *"it works fine, but not anymore"*, one file on the other side of the earth is not getting moved!
after reviewing all the logs and I confirm that it was not caused by my change, one destination was running out of space!

## What I learned

 - nobody knows all features without end-to-end tests. (I should know this from day 1, but I believe that by reading the code I could totally understand the app)A
 - no integration test / end-to-end test, which means the feedback is mostly triggered by production issue.
 - nobody wants to touch the code, not only because the risk of introducing bugs but also taking responsibility for the change


I refused to make any more changes -- until I automated all end-to-end test cases.

## What I did

 - built a BDD testing framework to enable me write all my known test cases in BDD/Gherkin style 
 - setup CI pipeline to execute automation tests on each code change 
 - documented most of the features in BDD/Gherkin style 
 - share the testing freamwork to users, let them to add test cases
 - share BDD with all developers, BDD feature file is mandatory for feature changes


## What I achieved
after few months:
 - the file mover has a CI pipeline with fully automated end-to-end tests. 
 - feature files are considered as documents. 
 - developers are comfortable to change the production code.
