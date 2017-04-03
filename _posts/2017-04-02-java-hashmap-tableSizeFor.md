---
layout: post
title:  "JDK HashMap中的算法(1): 获得等于或大于指定整数的2次冥"
date:   2017-04-02 23:00:00 +0800
categories: dev
tags: 
 - java
---

### 问题: 给定一个整数, 计算等于或大于这个整数的第一个2次冥

举例: 输入12, 输出16

### 解决思路: 

1. **循环, 直到找到下一个2的冥次方**

```java
for each int from i to MAX: 
    if isPowerOfTwo_1(i) => return i
```
在 is_power_of_2()复杂度为`O(1)`的情况下, 这个解决方案的复杂度为:　`O(n)`, 如: 

```java
public boolean isPowerOfTwo_1(int n) {
    return (n > 0) && (n & (n - 1)) == 0;
}
```

2. **使用Bitwise操作**

如果n是2的冥, 二进制表示会是这样:
```
2^0 1 = 0001
2^1 2 = 0010
2^2 4 = 0100
2^3 8 = 1000
```
因此, 给定一个`1***`, 只要拿到`1111`, 然后再加1就可以得到结果. 可以使用`Bitwise`的`移位`与`或` 操作

**答案**: [来自OpenJDK8 HashMap](http://grepcode.com/file_/repository.grepcode.com/java/root/jdk/openjdk/8u40-b25/java/util/HashMap.java/?v=source)

```java
/**
 * Returns a power of two size for the given target capacity.
 */
static final int tableSizeFor(int cap) {
    int n = cap - 1;
    n |= n >>> 1;
    n |= n >>> 2;
    n |= n >>> 4;
    n |= n >>> 8;
    n |= n >>> 16;
    return (n < 0) ? 1 : (n >= MAXIMUM_CAPACITY) ? MAXIMUM_CAPACITY : n + 1;
}

```

 - 一开始的`n = cap - 1`操作是为了应对`cap`已经是2次冥的情况, 这样就可以统一处理;
 - 注意边界值:如果输入为0, Bitwise操作结束后, `n = -1`
 
 在`HashMap`中, `tableSizeFor()`用于根据传入的`initialCapacity`计算`capacity`. 
 如 `map = HashMap(initialCapacity=20, loadFactor=0.8f)`, `capacity`将会在`resize()`时被设置为`tableSizeFor(20)`的结果, `32`.