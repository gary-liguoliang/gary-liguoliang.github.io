---
layout: post
title:  "Google Cloud Tasks: use queue.xml to control rate for slow queues"
date:  20200329 22:49:18 +0800
categories: default 
tags:
 - lessons-learned
 - GCP
---


We got a service that has an HTTP request rate limit: less than 1 message per 10 seconds. we don't use this service frequently,
but when we use it, we send two requests sequentially, as expected, we recevied few `http 429`. 

we want to use Google Tasks to control the rate. 

**First try**

I don't know much about `token bucket`, by glancing the help doc, I think it will help by
setting `--max-dispatches-per-second=0.01`  (1 message / 10 seconds) with:

```
cloud tasks queues update my-task-queue --max-concurrent-dispatches=1  --max-dispatches-per-second=0.01
```

however, we noticed that HTTP 429 persists after the change, task queue log shows tasks are dispatched almost at the same time.  until we checked the `maxBurstSize`: 

> Each queue has a token bucket that holds tokens, up to the maximum specified by maxBurstSize. Each time a task is dispatched, a token is removed from the bucket. Tasks will be dispatched until the queue's bucket runs out of tokens. The bucket will be continuously refilled with new tokens based on maxDispatchesPerSecond.
and this field is an `output` value of `gcloud`, `gcloud tasks queues describe my-task-queue` shows the `maxBurstSize` is 10.

so the bucket should have 10 tokens initially, even though I set the rate, but in my case, the first call will get run immediately because 10 tokens are available right there. 
read the document again, and I found:

> In most cases, using the Cloud Tasks API method and letting the system set max_burst_size produces a 
very efficient rate for managing request bursts. In some cases, however, particularly when the desired rate is relatively slow, either using the queue.yaml method to manually set bucket_size to a small value, 
or setting your max_concurrent_dispatches to a small value via the Cloud Tasks API can give you more control.
https://cloud.google.com/tasks/docs/configuring-queues#rate

**Second try**

set bucket_size to 1 using `queue.yaml`, task queue log shows tasks are dispatched right at the rate I set. 


**That's not all**,  you'd better to read this one before using queues.xml:

[Pitfalls of mixing queue.yaml and gcloud command](https://cloud.google.com/tasks/docs/queue-yaml#pitfalls)

and these posts also help:

- https://stackoverflow.com/questions/3740835/what-is-meant-by-bucket-size-of-queue-in-the-google-app-engine/3740846#3740846
- [a feature request:  Make Max Burst Size configurable](https://issuetracker.google.com/issues/138813037)
