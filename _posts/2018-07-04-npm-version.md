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


## prerelease tags and ranges

based on the following check:
```javascript
const semver = require('semver')
> semver.gt('1.1.1-rc.1', '1.1.0')
true
> semver.gt('1.1.2-rc.1', '1.1.1-rc.1')
true
> semver.gt('1.1.2-rc.2', '1.1.2-rc.1')
true
```

I would assume that given a list of versions:
`['1.1.0', '1.1.1-rc.3', '1.1.1-rc.2', '1.1.1-rc.1', '1.1.2-rc.1', '1.1.2-rc.2''`:

 - `>1.0` would return `1.1.2-rc.2`
 - `>1.1.1-rc.2` would return `1.1.2-rc.2`
 
 the acutal result is:
 ```
 > semver.maxSatisfying(['1.1.0', '1.1.1-rc.3', '1.1.1-rc.2', '1.1.1-rc.1', '1.1.2-rc.1', '1.1.2-rc.2'], '>1.0')
'1.1.0'
> semver.maxSatisfying(['1.1.0', '1.1.1-rc.3', '1.1.1-rc.2', '1.1.1-rc.1', '1.1.2-rc.1', '1.1.2-rc.2'], '>1.1.1-rc.2')
'1.1.1-rc.3'

// add 1.2.0 to the version list
> semver.maxSatisfying(['1.1.0', '1.1.1-rc.3', '1.1.1-rc.2', '1.1.1-rc.1', '1.1.2-rc.1', '1.1.2-rc.2', '1.2.0'], '>1.1.1-rc.2')
'1.2.0'
```

**possiable to get the latest pre release based on a versin range?**
the answer is No.

> If a version has a prerelease tag (for example, 1.2.3-alpha.3) then it will only be allowed to satisfy comparator sets if at least one comparator with the same [major, minor, patch] tuple also has a prerelease tag.

> For example, the range >1.2.3-alpha.3 would be allowed to match the version 1.2.3-alpha.7, but it would not be satisfied by 3.4.5-alpha.9, even though 3.4.5-alpha.9 is technically "greater than" 1.2.3-alpha.3 according to the SemVer sort rules. The version range only accepts prerelease tags on the 1.2.3 version. The version 3.4.5 would satisfy the range, because it does not have a prerelease flag, and 3.4.5 is greater than 1.2.3-alpha.7.

> The purpose for this behavior is twofold. First, prerelease versions frequently are updated very quickly, and contain many breaking changes that are (by the author's design) not yet fit for public consumption. Therefore, by default, they are excluded from range matching semantics.

> Second, a user who has opted into using a prerelease version has clearly indicated the intent to use that specific set of alpha/beta/rc versions. By including a prerelease tag in the range, the user is indicating that they are aware of the risk. However, it is still not appropriate to assume that they have opted into taking a similar risk on the next set of prerelease versions.

semver.js source code: 
https://github.com/npm/node-semver/blob/v5.5.0/semver.js#L1121
