---
layout: post
title:  "在银行做DevOps"
date:   2017-04-09 22:00:00 +0800
tags: 
 - DevOps
---

几个月前, 我换到了现在的DevOps team, 与Dev, QA, Ops一起, 运维一个庞大的银行前台系统. 

### 做什么?

![pipeline](https://d0.awsstatic.com/product-marketing/DevOps/DevOps_feedback-diagram.png)
上图来自[AWS:What is DevOps?](https://aws.amazon.com/devops/what-is-devops/)

DevOps是什么? 有人玩笑说： 开发者做运维．这的确是我的经历, 之前是developer, 现在做ops. 几个月下来，我所理解的DevOps：
负责代码提交之后的工作:　提供打包，测试，发布，生产环境监控/支撑一条龙服务.

今天聊聊测试与发布.

### 提供测试服务 Test as a Service

跟很多团队一样, 我们也在努力的实践TDD, BDD. 新的功能应该从feature file开始, 不断的迭代、验证, 而不是先开发后验证. DevOps团队需要支撑测试, 提供测试所需的工具与环境.

#### 开发测试套件

对于很多早已上线的App以及Legacy系统, 我们需要从新增加feature test来确保其正常运行.  这些feature test往往需要非常深厚的专业知识, 所以不管是Dev,Ops还是DevOps, 都写不了feature file. 这些工作由BA(Business Analyst)负责. 他们会与最终用户沟通需求, 然后编写[Gherkin feature file](https://github.com/cucumber/cucumber/wiki/Feature-Introduction).

有很多敏捷团队会提倡`Wearing Multiple Hats`, 或者说人人都是`Developer`(前几年我在摩根大通工作时, 很多团队就提倡人人都是developer). 这样的做法可能适合某些场景, 但是在某些专业领域并不适用: 有些产品太过专业, developer/coder只能了解一部分功能, 而不能整体把握整体的商业流程. 

但BA不会写代码, 我们也不能跟在BA后面等feature test写好再实现, 所以DevOps开发测试套件, 内置测试所需的大部分语法, **BA只需要根据已有的语法, 就能独立编写并运行测试.** 

#### 支撑测试环境

我们对测试环境有近乎生产环境的苛刻要求. 因为有些重要的测试会耗费大量资源(譬如: 几千个核), 或者耗费大量时间(几小时)

我很羡慕那些能够完全自动化的系统, 一个command就可以把整个系统部署起来. 很可惜, 我们的系统有太多的依赖: 依赖庞大的数据库, 消息队列, 下游系统. 一个标准的测试环境需要一个集群, 为了保证测试准确性, 应用程序, 数据库, 下游系统都需要整齐划一的运行.

即使存在这么多的限制, DevOps还是要尽多尽早的部署新的release candidate. 为了规避来自其他服务或应用的风险, DevOps会尽可能多的监控测试环境. 

#### CI

除了开发测试套件与支撑测试环境, DevOps还会维护一个CI服务, 以便BA可以自己配置CI工程, 来运行他们的测试. TeamCity是一个不错的选择, 相比Jenkins, TeamCity对非技术人员更友好一些.   


### 发布 Release

在银行工作过的同学都应该了解, release不是想做就能做的. 需要根据合规/审计部门的要求, 提前计划, 获得层层批准. DevOps需要在规定时间内完成所有操作. 如果需要手动的复制文件, 手动的安装应用, 那将会一场噩梦. 
我们使用Python根据内部需要, 开发了自动化发布系统, 除此之外, 我们也通过减小测试环境与生产环境的差别来降低风险. 
 
我们的部署工具随着一次次的部署而不断改进, 在这一过程中, 我们学到很多经验, 如: 
 - 不要假设生产环境会有怎样的配置. 如果有疑问, 应该尽早确认
 - 消除一切能消除的生产/测试环境差别
 - 不要存在重复代码, 看似复制粘贴很快, 实际上就是在挖坑
 - 减少`if...else...` 尤其是在配置文件中, 如: `if env.is_prod()...else...`, 因为这样的代码没法在生产环境之外测试

### 话题

**缩小Feedback loop, 每个人都是受益者, 每个人都需要参与**

如果你是一个developer, 有没有想过这个问题: 既然有integration test, 我们还需要写unit test吗? 
我相信很多人都像曾经的我一样, 认为既然有足够的integration test就能保证万无一失, unit test并不是必须的. 

如果project变大变复杂, 你就会发现, 不写unit test的成本是很高的: 假如小明不小心增加了一个bug, 如: `amount_in_sgd = amount_in_usd * rate_usd_cny`(新币金额 = 美元金额 * 美元对人民币汇率). 小明赶进度, 没写测试就check-in, 小花也忙着自己的工作, 扫了一眼, 就批准了小明的代码, 是bug就进入了系统. 
紧接着, 系统build(5分钟), 基本测试(15分钟)通过. 小明已经全力以赴的开始了下一个task. 基本测试成功后的artifact被部署到测试环境中, 连接上下游系统, 开始跑集成测试, 40分钟之后, 小明收到邮件, 从进行到一半的任务中抽身回来检查bug.([Context switch](http://blog.trello.com/why-context-switching-ruins-productivity)) 这个feedback花了60分钟才收到!
这还是理想情况, 如果中间夹杂有任何的异常, 这个feedback都会被拖延. 而且这里有一个假设: 集成测试涵盖了所有的测试项目. 如果这样的bug没有在集成测试里发现, 恐怕到生产环境, 用户才会发现, 这时候这个feedback就升级成了production issue. 

所以测试要早做, 离production code越近越好. 小明如果编写UnitTest, 他就可以在几秒钟之内获得feedback. 有效的规避之后的context switch以及其他风险. 在现实生活中也是这样: 假如你买到一辆发动机有问题的汽车, 你会是什么感觉? 你可能会很生气, 因为汽车厂商没有做好他们该做的: 测试并保证质量. 如果你是负责发动机的工程师, 你一定会在发动机装进整车之前就做好测试.
对DevOps来说, 更是这样. 我们不会假设一个release candidate是完美的, 所以先会把release candidate放到一个CI环境里去跑, 快速部署, 快速测试, 尽量缩小feedback loop. 

**协作**

在设计新功能时, Development team应该从尽早邀请DevOps/Ops介入, 至少进行Design Review, DevOps会站在不同的立场上来看待每一个新功能, 提出建议. 这些建议往往对于系统的维护运行都很重要, 一个没有兼顾到Ops的设计, 很可能是在埋坑.
 
**重写还是重构 Rewrite or Refactor?**

> "这个application写的太烂了, 我们应该从头开始重新写"

听起来拫熟悉吧? 总会有人(尤其是新人)无法忍受旧的程序, 提议重新来过, 可问题是: 真的需要吗? 以我的经验, 这大多时候是在用另一种语言/框架来犯相同的错误. 
> [Jel on software:](https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/) 
> It’s important to remember that when you start from scratch there is absolutely no reason to believe that you are going to do a better job than you did the first time. First of all, you probably don’t even have the same programming team that worked on version one, so you don’t actually have “more experience”. You’re just going to make most of the old mistakes again, and introduce some new problems that weren’t in the original version.
 