---
layout: post
title:  "How HashMap works in Java"
date:   2017-03-30 23:00:00 +0800
categories: dev
tags: 
 - java
---

How many times have been asked this question in your job interview? for me, more than 10.  I want to be crystal clear about this question to save everyone's time. 

## How HashMap works in Java? 

`HashMap` is a `key-value` pair container based on hash table. it usually acts as a binned(bucketed) hash table, but when bins get too large, 
they are transformed into bins of `TreeNodes`. a typical HashMap looks like:
![HashMap](https://raw.githubusercontent.com/guoliang-dev/guoliang-dev.github.io/master/resources/java-hashmap.PNG)

### the hash table
the `table` acts as the index, initialized on first use, e.g. `put(key, value)`. the default capacity is `16`.

let's say we initialized a map: `Map<User, String> map = new HashMap<>()`, and now we want to `map.put(user1, "emai-add")`
first thing for a `put` is to identify the location in the `table`.  which cell should we put the `Node<key, value>`? 

### identify index in the hash table
```java
//  Computes key.hashCode() and spreads (XORs) higher bits of hash to lower.
hash = (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16)
index = (table.length - 1) & hash
```
the `index` is calculated from the `key.hashCode()`, and the table `length`. `h >>> 6` spreads higher bits of has to lower: 
> the table uses power-of-two masking, sets of hashes that vary only in bits above the current mask will always collide

![HashMap-identify-index](https://raw.githubusercontent.com/guoliang-dev/guoliang-dev.github.io/master/resources/java-hashmap-identify-index.PNG)


### attache the node

if the cell `table[index]` is empty, we can directly put a `Node(key, value)`, e.g.
```java
table[index] = newNode(hash, key, value, null);
```

if the cell already occupied, check the nodes and update/insert new node:

```java
p = table[index]
Node<K,V> e; K k;
if (p.hash == hash && ((k = p.key) == key || (key != null && key.equals(k))))
    e = p;
else if (p instanceof TreeNode)
    e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
else {
    for (int binCount = 0; ; ++binCount) {
        if ((e = p.next) == null) {
            p.next = newNode(hash, key, value, null);
            if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
                treeifyBin(tab, hash);
            break;
        }
        if (e.hash == hash &&
            ((k = e.key) == key || (key != null && key.equals(k))))
            break;
        p = e;
    }
}

if (e != null) { // existing mapping for key
    V oldValue = e.value;
    if (!onlyIfAbsent || oldValue == null)
        e.value = value;
    afterNodeAccess(e);
    return oldValue;
}

if (++size > threshold)
    resize();

```

the key-value pair `Node<user1, "eamil-add">` is attached on the hash table now. 

at the end of `put` method, `HashMap` will check whether it needs a `resize()` 


### resize if necessary

power-of-two expansion, elements from each bin must either stay at same index, or move with a power of two offset in the new table.

![HashMap-resize](https://raw.githubusercontent.com/guoliang-dev/guoliang-dev.github.io/master/resources/java-hashmap-resize.PNG)

```java
@SuppressWarnings({"rawtypes","unchecked"})
    Node<K,V>[] newTab = (Node<K,V>[])new Node[newCap];
table = newTab;
if (oldTab != null) {
    for (int j = 0; j < oldCap; ++j) {
        Node<K,V> e;
        if ((e = oldTab[j]) != null) {
            oldTab[j] = null;
            if (e.next == null)
                newTab[e.hash & (newCap - 1)] = e;
            else if (e instanceof TreeNode)
                ((TreeNode<K,V>)e).split(this, newTab, j, oldCap);
            else { // preserve order
                Node<K,V> loHead = null, loTail = null;
                Node<K,V> hiHead = null, hiTail = null;
                Node<K,V> next;
                do {
                    next = e.next;
                    if ((e.hash & oldCap) == 0) {
                        if (loTail == null)
                            loHead = e;
                        else
                            loTail.next = e;
                        loTail = e;
                    }
                    else {
                        if (hiTail == null)
                            hiHead = e;
                        else
                            hiTail.next = e;
                        hiTail = e;
                    }
                } while ((e = next) != null);
                if (loTail != null) {
                    loTail.next = null;
                    newTab[j] = loHead;
                }
                if (hiTail != null) {
                    hiTail.next = null;
                    newTab[j + oldCap] = hiHead;
                }
            }
        }
    }
}
```
