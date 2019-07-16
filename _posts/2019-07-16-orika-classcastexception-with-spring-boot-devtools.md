---
layout: post
title:  "Orika with Spring-boot Devtools MappingException/ClassCastException: Mapper Cannot be Cast to GeneratedObjectBase"
date:  20190716 22:16:50 +0800
categories: deault 
tags:
 - java
 - spring
 - class-loader
---

I was trying to run a spring-boot application which uses an Orika mapper from one of it's dependencies (the dependency is released as a jar):
```
Caused by: ma.glasnost.orika.MappingException: java.lang.ClassCastException: ma.glasnost.orika.generated.Orika_UserDest_UserSource_Mapper3053159455512$0 cannot be cast to ma.glasnost.orika.impl.GeneratedObjectBase
	at ma.glasnost.orika.impl.generator.MapperGenerator.build(MapperGenerator.java:104) ~[orika-core-1.5.1.jar:na]
	at ma.glasnost.orika.impl.DefaultMapperFactory.buildMapper(DefaultMapperFactory.java:1480) ~[orika-core-1.5.1.jar:na]
	at ma.glasnost.orika.impl.DefaultMapperFactory.build(DefaultMapperFactory.java:1295) ~[orika-core-1.5.1.jar:na]
	at ma.glasnost.orika.impl.DefaultMapperFactory.getMapperFacade(DefaultMapperFactory.java:883) ~[orika-core-1.5.1.jar:na]
	at ma.glasnost.orika.impl.ConfigurableMapper.init(ConfigurableMapper.java:121) ~[orika-core-1.5.1.jar:na]
	at ma.glasnost.orika.impl.ConfigurableMapper.<init>(ConfigurableMapper.java:97) ~[orika-core-1.5.1.jar:na]
	at com.liguoliang.common.mapper.UserMapper.<init>(UserMapper.java:8) ~[common-1.0-SNAPSHOT.jar:na]
	at com.liguoliang.springboot1.helloworld.TestApp.run(TestApp.java:30) ~[classes/:na]
	at org.springframework.boot.SpringApplication.callRunner(SpringApplication.java:732) [spring-boot-1.5.15.RELEASE.jar:1.5.15.RELEASE]
	... 11 common frames omitted
Caused by: java.lang.ClassCastException: ma.glasnost.orika.generated.Orika_UserDest_UserSource_Mapper3053159455512$0 cannot be cast to ma.glasnost.orika.impl.GeneratedObjectBase
	at ma.glasnost.orika.impl.generator.SourceCodeContext.getInstance(SourceCodeContext.java:262) ~[orika-core-1.5.1.jar:na]
	at ma.glasnost.orika.impl.generator.MapperGenerator.build(MapperGenerator.java:73) ~[orika-core-1.5.1.jar:na]
	... 19 common frames omitted
```
I was confused by this error because the class `Orika_UserDest_UserSource_Mapper3053159455512$0` obviously is a generated class and it supposed to work with Orika itself.


to illustrate the project structure:

the spring-boot I'm currently working on:
```
<project>
	<groupId>com.liguoliang</groupId>
	<artifactId>spring-boot-1.5-hello-world</artifactId>
	<version>0.0.1-SNAPSHOT</version>
	<packaging>jar</packaging>

	<parent>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-parent</artifactId>
		<version>1.5.15.RELEASE</version>
		<relativePath/> <!-- lookup parent from repository -->
	</parent>

	<dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
		<dependency>
			<groupId>com.liguoliang</groupId>
			<artifactId>common-demo</artifactId>
			<version>0.0.1</version>
		</dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <optional>true</optional>
        </dependency>
    </dependencies>
 </project>
```

the dependency jar file's pom: (which is where the mapper come form):
```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.liguoliang</groupId>
    <artifactId>common-demo</artifactId>
    <version>0.0.1</version>

    <packaging>jar</packaging>

    <dependencies>
        <dependency>
            <groupId>net.rakugakibox.spring.boot</groupId>
            <artifactId>orika-spring-boot-starter</artifactId>
            <version>1.5.0</version>
        </dependency>
    </dependencies>
</project>
```

## What I found by debugging

the issue happens here:
```
// SourceCodeContext.java
    public <T extends GeneratedObjectBase> T getInstance() throws SourceCodeGenerationException, InstantiationException,
            IllegalAccessException {
        T instance = (T) compileClass().newInstance();
        ...
        }
```
the `compileClass()` shows that the source of the generated class is:
```
package ma.glasnost.orika.generated;
public class Orika_UserDest_UserSource_Mapper3053159455512$0 extends ma.glasnost.orika.impl.GeneratedMapperBase {
...
```
`GeneratedMapperBase` extends `GeneratedObjectBase`, by reading the code, I'm sure that `compileClass().newInstance()` must be a `GeneratedObjectBase` .

but issue happened, consistently. in the runtime, instance a of A is not a A, that could be caused by A was loaded in multiple loader? I found:
 - `GeneratedClass.class` was loaded by `Launcher$AppClassLoader`
 - `compileClass()` and `compileClass().getSuperclass().getSuperclass()`(which is `GeneratedObjectBase`) were loaded by `RestartClassLoader`, `RestartClassLoader.parent` is the `Launcher$AppClassLoader`

so the error message can be enhanced to show that:
**jvm failed to cast instance of `GeneratedObjectBase` loaded by `RestartClassLoader` to `GeneratedObjectBase` loaded by `AppClassLoader`**

## Why `GeneratedObjectBase` got loaded by two different class loaders?

 - before the mapper get actually initialized, the mapper(part of the common-demo lib) get loaded by `AppClassLoader`, probably together with the mapper, `GeneratedClassBase` also get loaded by `AppClassLoader`
 - when the mapper getting initialized, [spring-boot devtools](https://docs.spring.io/spring-boot/docs/current/reference/html/using-boot-devtools.html#using-boot-devtools-customizing-classload) will use the `RestartClassLoader` to load classes in the workspace of the IDE, to get faster 'reload':
    - Orika used the `RestartClassLoader` to compile the generated class:
      ```
       // JavassistCompilerStrategy.compileClass()
        compiledClass = byteCodeClass.toClass(Thread.currentThread().getContextClassLoader(), this.getClass().getProtectionDomain());
      ```
      so the generated class and the parent classes all get loaded by `RestartClassLoader`
 that how did the exception happen.

## How to fix?
 - disable spring-boot devtools with `-Dspring.devtools.restart.enabled=false`, which will disable the `RestartClassLoader`, but lost the faster reload feature.
 - [include the dependency jar file to `restart.include` in `META-INF/spring-devtools.properties`](https://docs.spring.io/spring-boot/docs/current/reference/html/using-boot-devtools.html#using-boot-devtools-customizing-classload), which will let `RestartClassLoader` to load the mapper.

## Conclusion

Restart functionality from Spring-boot devtools can be very helpful when working in an IDE, the application get restarted automatically on class change.
however issues can happen when class loaders get messed up. e.g. due to the dependency structure, `GeneratedObjectBase` was loaded by two loaders which caused the exception.

