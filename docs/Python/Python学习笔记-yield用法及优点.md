# Python学习笔记-yield用法及优点

## 概述

`yield` 用于定义生成器，它最终返回一个生成器对象，这个生成器对象可以被迭代。

## 例子

```python
# encoding:utf8
import sys

n = 200
m = 1000
# 定义一个生成器，yield必须在函数中使用
def Generators(n):
    for i in range(n):
        if i%2==0:
            yield i
print("参数为200生成器占用内存大小：",sys.getsizeof(Generators(n)))
print("参数为1000生成器占用内存大小：",sys.getsizeof(Generators(m)))

# 创建一个列表对象
listobj_1 = [i for i in range(n) if i%2==0]
listobj_2 = [i for i in range(m) if i%2==0]
print("参数为200列表占用内存大小：",sys.getsizeof(listobj_1))
print("参数为1000列表占用内存大小：",sys.getsizeof(listobj_2))
```

## 运行结果

```
参数为200生成器占用内存大小： 200
参数为1000生成器占用内存大小： 200
参数为200列表占用内存大小： 920
参数为1000列表占用内存大小： 4216
```

## 优点

1. 内存效率：执行结果占用内存不一致，当数据量越大，列表占用的内存就越大，而生成器占用的内存基本上是恒定的
2. 惰性求值：只在进行迭代时才生成计算结果，避免无效的计算
3. 无限序列：对序列长度没有限制

