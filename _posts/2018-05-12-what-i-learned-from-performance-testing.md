---
layout: post
title:  "What I Learned from a Performance Testing"
date:  2018-05-12 23:00:00 +0800
categories: test
tags:
 - test
---

I recently joined a new team as a do-everything engineer. The team is trying hard to push a newly web app to production. the app enables existing users buy products which are provides by an external vendor. the app  relies on existing authentication services, payment services, order services, etc. 

After spending couple weeks with an existing 'Performance testing' team, I finally get the test 'approved'. I learned couple things from this process. 

## if downstream services are not available for testing, mock it. 

or else the performance tet won't happend at all. given the following diagram, it's almost impossiable to get all dependencies ready for my testing, e.g:
 - UserService has a testing envrioment for us, but it took days to request a test user. 
 - PaymentGateway need UserInfo ready and all test data will be created manully --- an account could run out of money in the middle of a performance test.  
 
agreed with core stockholders, I performed the test with: `the app itself + mocked (existing) internal services + real external services. `

```
+-----+         +-----------------------+              +-------------+ +-------------------------+ +-----------------------+                   +-----------------+ +-----------------------+
| App |         | AuthenticationService |              | UserService | | ExternalProductService  | | InternalOrderService  |                   | PaymentGateway  | | ExternalOrderService  |
+-----+         +-----------------------+              +-------------+ +-------------------------+ +-----------------------+                   +-----------------+ +-----------------------+
   |                        |                                 |                     |                          |                                        |                      |
   |                        |                                 |                     |                          |                                        |                      |
   |                        |                                 |                     |                          |                                        |                      |
   | user login             |                                 |                     |                          |                                        |                      |
   |----------------------->|                                 |                     |                          |                                        |                      |
   |                        |                                 |                     |                          |                                        |                      |
   |                        | user info verify request        |                     |                          |                                        |                      |
   |                        |-------------------------------->|                     |                          |                                        |                      |
   |                        |                                 |                     |                          |                                        |                      |
   |                        |                        verified |                     |                          |                                        |                      |
   |                        |<--------------------------------|                     |                          |                                        |                      |
   |                        |                                 |                     |                          |                                        |                      |
   |                 tokens |                                 |                     |                          |                                        |                      |
   |<-----------------------|                                 |                     |                          |                                        |                      |
   |                        |                                 |                     |                          |                                        |                      |
   | get user info          |                                 |                     |                          |                                        |                      |
   |--------------------------------------------------------->|                     |                          |                                        |                      |
   |                        |                                 |                     |                          |                                        |                      |
   |                        |                       user info |                     |                          |                                        |                      |
   |<---------------------------------------------------------|                     |                          |                                        |                      |
   |                        |                                 |                     |                          |                                        |                      |
   | fetch products         |                                 |                     |                          |                                        |                      |
   |------------------------------------------------------------------------------->|                          |                                        |                      |
   |                        |                                 |                     |                          |                                        |                      |
   |                        |                                 |            products |                          |                                        |                      |
   |<-------------------------------------------------------------------------------|                          |                                        |                      |
   |                        |                                 |                     |                          |                                        |                      |
   | user place order       |                                 |                     |                          |                                        |                      |
   |---------------------------------------------------------------------------------------------------------->|                                        |                      |
   |                        |                                 |                     |                          |                                        |                      |
   |                        |                                 |                     |                          | verify toke / payment request          |                      |
   |                        |                                 |                     |                          |--------------------------------------->|                      |
   |                        |                                 |                     |                          |                                        |                      |
   |                        |                                 |                     |                          |                      payment processed |                      |
   |                        |                                 |                     |                          |<---------------------------------------|                      |
   |                        |                                 |                     |                          |                                        |                      |
   |                        |                                 |                     |                          | place order                            |                      |
   |                        |                                 |                     |                          |-------------------------------------------------------------->|
   |                        |                                 |                     |                          |                                        |                      |
   |                        |                                 |                     |                          |                                        |   order confirmation |
   |                        |                                 |                     |                          |<--------------------------------------------------------------|
   |                        |                                 |                     |                          |                                        |                      |
   |                        |                                 |                     |       order confirmation |                                        |                      |
   |<----------------------------------------------------------------------------------------------------------|                                        |                      |
   |                        |                                 |                     |                          |                                        |                      |
   ```

## Performance testing should be conducted from Day 1

during the performance testing, one slowness issue was detected: it took quite long time to get user info from the mocked UserService. the mocked UserService does very straightforward job: returning a fixed user info from localhost. so it's isolated, the issue must be caused the app itself. 
I reviewed the sourcecode, an uncessary synchronization was applied to the servlet.  it was added in the first commit half year ago, the feedback loop for this piece of code is: 6 months.  

if we setup all mocked services and run PT as part of the DevOps pipeline, this issue could be indentified and fixed in the fist PT. 

## Performance testing should be automated

it took me couple days to help the perfromance testing team understand the app, then they spend couple days to perpare their test cases. and if there's any change to the app. I need to go though the whole process with them again. this does not make sense to me: as an agile team, we're moving fast, but if it took couple days(even weeks) to test, the test result is not valid anymore when the test finish --- more changes already appied to the app.  same as other tests, performance test should be auomated. it should be executed by a machine, not by a team. the result should be 
