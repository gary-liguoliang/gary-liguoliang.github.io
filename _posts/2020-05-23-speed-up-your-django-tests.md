---
layout: post
title:  "Speed Up Your Django Tests"
date:  20200523 17:14:18 +0800
categories: default 
tags: Python, Django
---

I read the book [“Speed Up Your Django Tests”](https://gumroad.com/l/suydt?utm_source=liguoliang.com) this week, a few interesting items: 

**Background/disclaimer**:
*I'm new to Django,  I use `pytest` to run many integration Django tests. so the points listed here are purely from my point of view.*

1. Override settings: with `@override_settings`,  [in case you want to override a setting for a test method, Django provides the override_settings() decorator (see PEP 318).](https://docs.djangoproject.com/en/3.0/topics/testing/tools/#django.test.override_settings)
2. Show slow tests with `pytest --durations 10`
3. Tests marker, categorize/tag tests so that can run different subsets.  like JUnit categories
for more details: https://docs.pytest.org/en/latest/example/markers.html
4. Reduce pytest test collection by setting `norecursedirs`
5. Run in parallel with `pytest-xdist`
6. **Django’s `RequestFactory`**: This is similar to the test client, but instead of making requests, "provides a way to generate a request instance that can be used as the first argument to any view"
[Django Doc](https://docs.djangoproject.com/en/3.0/topics/testing/advanced/#the-request-factory)
7. **Django’s `SimpleTestCase`**:  a subclass of `unittest.TestCase`, it "disallows database queries by default.",  however, you till can turn it on.
8. **Avoid Fixture Files**[11.1],  "For data you need in individual tests, you’re better off creating it in the test case or test method."  I have to see it's very easy to set up test data with `fixtures`, but shortly it becomes unmanageable few valid points: 

  > Fixture ˉles are separate from the tests that use them. This makes it hard to determine which tests use which objects. The ˉles tend to become “append-only,”...when a new test needs a new object, it tends to be added to an existing file...if there’s some data that most of your application depends on, using a fixture, causes unnecessary reloading. It will be loaded and then rolled back for each test case, even when the next test case needs the exact same data.
  
The book also covers many other topics, such as "Profiling", "Mocking" etc, and many topics and links for me to explore Django. overall, I would say it's a good Django testing book for newbies like me.
