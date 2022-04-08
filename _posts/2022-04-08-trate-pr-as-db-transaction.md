---
layout: post
title:  "Pull requests should be treated as database translation: all kinds of changes should be included"
date:  20220408 23:30:00 +0800
categories: default
tags:
 - Python
---

A few weeks ago, I received a request to update the pricing logic for certain products. I made the code change, a silly example:

```python
def get_price(product: Product) -> Decimal:
    if product.pricing_stragety == "10-percent-off":
        return product.price * Decimal("0.9")
    else:
        return product.price
```

of course, I also have unit tests to cover the change, everything is fine, so I pushed to production and told my business users that everything is sorted out. 
I know I also need to update the product configs in database, but I think I can do it manually right after the release.  

but I didn't, before I get back to the "manual" change in db, a production issue reported:  price is not discounted, customers are not happy.  then I spent hours to fix all the impacted orders.

I cloud easily avoid this issue by adding a db migration script into my pull request. the lesson I learned is to treat a pull request as a database transaction,  should contain all changes: code, data, infra etc,.

