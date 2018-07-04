---
layout: post
title:  "npm versioning"
date:  2018-07-04 23:00:00 +0800
categories: dev
tags:
 - npm
---

## npm versioning

https://docs.npmjs.com/getting-started/semantic-versioning

[major, minor, patch] 

e.g. 
 - fist release: 1.0.0
 - bug fix, minor change -> 1.0.1, 1.0.2
 - non-breaking new features -> 1.1.0
 - breaking changes -> 2.0.0

**Semver for Consumers**

 - [different ways to define semantic versiong](https://docs.npmjs.com/misc/semver)
 - [npm semver calculator](https://semver.npmjs.com/)

## update dependencies based on semantic versions

`npm install`:
> npm will look at the dependencies that are listed in that file and download the latest versions, using semantic versioning.
(https://docs.npmjs.com/getting-started/using-a-package.json#managing-dependency-versions)

`yarn upgrade`:
> Upgrades packages to their latest version based on the specified range.
(https://yarnpkg.com/lang/en/docs/cli/upgrade/)


