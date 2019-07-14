---
layout: post
title:  "Always Check Build Lock File into Source Control"
date:  20190714 23:42:00 +0800
categories: default
tags:
 - CI
---

one of my teammates (a frontend developer) came to me with question: "why my CI build is failing? it was fine yesterday and I just tried it works fine locally!"

I don't have much experience with the frontend, but I don't believe any magic in computer science, everything has a reason, so I stopped my task and start reading the CI output:
```
> no yarn.lock detected, using npm
> npm run build
.....
...another-lib.js v1.3.1
```

humm, then I questioned back to my teammate, "how did you build your local project? ", "yarn build".
I found "another-lib.js 1.3.0" in his local `yarn.lock` file, and as the ci output pointed out: yarn.lock is not version controlled.

## why a build lock file has to be checked in?

> All yarn.lock files should be checked into source control (e.g. git or mercurial). This allows Yarn to install the same exact dependency tree across all machines, whether it be your coworker’s laptop or a CI server.
(https://yarnpkg.com/lang/en/docs/yarn-lock/#toc-check-into-source-control)

## Conclusions
I never used yarn before, but the fist listen I learned is: commit yarn.lock file!
[Please commit your yarn.lock files](https://yarnpkg.com/blog/2016/11/24/lockfiles-for-all/)

