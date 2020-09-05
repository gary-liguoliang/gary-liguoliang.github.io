---
layout: post
title:  "Server-side GraphQL Journey in Python"
date:  20200905 10:19:00 +0800
categories: default
tags:
 - GraphQL
 - Python
 - Graphene
 - Ariadne
---

After playing around with few Python GraphQL libraries for a few weeks,  I realized that a good GQL python lib should:
    - be less invasive, work on top of the existing stack (FastAPI/starlette), reuse as much code as possible(Pydantic)
    - generate GQL schema from python code, ideally from built-in types and Pydantic types
    - supports `Subscriptions` out of the box


Currently, I’m happy with `Ariadne` in a code-first approach.  This post tracks the journey with issues we found and the workarounds/solutions.


# Graphene

Both [graphql.org](https://graphql.org/code/#python) and [fastapi](https://fastapi.tiangolo.com/advanced/graphql/) point to https://graphene-python.org/, so we get started with it. 

as you may or may not know, GraphQL has a concept called "Schema",  `Graphene` took "a code-first approach", which is cool:  

> Instead of writing GraphQL Schema Definition Language (SDL), we write Python code to describe the data provided by your server.


## Hello world works weel, but it's too verbose

```python
import graphene

class Query(graphene.ObjectType):
  hello = graphene.String(name=graphene.String(default_value="World"))

  def resolve_hello(self, info, name):
    return 'Hello ' + name
  

schema = graphene.Schema(query=Query)
result = schema.execute('{ hello }')
print(result.data['hello']) # "Hello World"
```

Looks simple yet still complex.  there're too many `graphene`s, why I need to learn another typing system?  which can be done by the framework,  what about this one? 

```python
# hello = graphene.String(name=graphene.String(default_value="World"))
hello: str = "World" 
```

## Reuse Pydantic types with graphene-pydantic

Since we're using `Pydantic`,  which has all the typing details, why not simply use `Pydantic`?! `https://github.com/graphql-python/graphene-pydantic` is exactly what we need! but even with `graphene-pydantic` an adaptor layer is required between `Pydantic` and `Graphene`, e.g.: 

```python

class PersonInput(PydanticInputObjectType):
    class Meta:
        model = PersonModel
        # exclude specified fields
        exclude_fields = ("id",)

class CreatePerson(graphene.Mutation):
    class Arguments:
        person = PersonInput()
    # more code trimmed
```

Still very verbose, but much better than the original one. 


## Subscriptions is not well supported yet

The document is super confusing: https://docs.graphene-python.org/projects/django/en/latest/subscriptions/:
>  To implement websocket-based support for GraphQL subscriptions, you’ll need to do the following:
Install and configure django-channels.
Install and configure* a third-party module for adding subscription support over websockets. A few options include:
graphql-python/graphql-ws
datavance/django-channels-graphql-ws
jaydenwindle/graphene-subscriptions
Ensure that your application (or at least your GraphQL endpoint) is being served via an ASGI protocol server like daphne (built in to django-channels), uvicorn, or hypercorn.
* Note: By default, the GraphiQL interface that comes with graphene-django assumes that you are handling subscriptions at the same path as any other operation (i.e., you configured both urls.py and routing.py to handle GraphQL operations at the same path, like /graphql).

what? why Django gets mentioned? I'm not interested and I'm lost!


Maybe it's time to move on. 


# Ariadne

This is from the Graphene's "Getting started": 

> Compare Graphene’s code-first approach to building a GraphQL API with schema-first approaches like Apollo Server (JavaScript) or Ariadne (Python). Instead of writing GraphQL Schema Definition Language (SDL), we write Python code to describe the data provided by your server.


Yeah, schema-first is not cool, but `Ariadne`'s documetation looks much better than Graphene.

## Subscriptions, it just works

After the experience with Graphene, the first feature I check was subscriptions:   https://ariadnegraphql.org/docs/subscriptionsit's simple and it just works!  the documentation is clean and no `django` mentioned at all!

```python
import asyncio
from ariadne import SubscriptionType, make_executable_schema
from ariadne.asgi import GraphQL

type_def = """
    type Query {
        _unused: Boolean
    }

    type Subscription {
        counter: Int!
    }
"""

subscription = SubscriptionType()

@subscription.source("counter")
async def counter_generator(obj, info):
    for i in range(5):
        await asyncio.sleep(1)
        yield i


@subscription.field("counter")
def counter_resolver(count, info):
    return count + 1


schema = make_executable_schema(type_def, subscription)
app = GraphQL(schema, debug=True)
```

## Schema first? it doesn't have to be

What if I change the `counter_generator` to return `str`? I need to update the Schema. if I forgot that, I'm lying to my users.  I hate it. 


In the above example, `type_def` is kind fo the duplication of the method `counter_generator` (if we add return type) like: 

```python
async def counter_generator(obj, info) -> int
```

the Schema looks reasonably easy to generate, why cannot we generate a schema from python code? especially with `Pydantic`?
if we define a method with proper tying, we cloud to generate the Schema easily: 
```python

class HelloMessage(BaseModel):
    body: str
    from_user: UUID


query = QueryType()


@query.field('hello')
def resolve_hello(_, info) -> HelloMessage:
    request = info.context['request']
    user_agent = request.headers.get('user-agent', 'guest')
    return HelloMessage(
        body='Hello, %s!' % user_agent,
        from_user=uuid4(),
    )


# Generate type_defs from Pydantic types in the query definition.
type_defs = generate_gql_schema_str([query])

schema = make_executable_schema(
    type_defs, query, snake_case_fallback_resolvers,
)
app = GraphQL(schema, debug=True)
```

the details could be found here: https://github.com/gary-liguoliang/ariadne-pydantic/blob/master/example/main.py


**With a small schema generation utility,  we managed to run `Ariadne` in a `code-first` approach**: 
 - Code is much simpler than the original version of both `Ariadne` and `Graphene` 
 - Resuing Pydantic typing 
 - the GQL query definition method is very simple, take input, forward to the core application, return the output. 
