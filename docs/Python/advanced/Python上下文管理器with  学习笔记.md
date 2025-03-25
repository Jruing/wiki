# Python上下文管理器with  学习笔记

`with` 这个关键字,很多人应该都用这个关键打开过文件,如下面的例子

```python
with open('test.txt','r',encoding:"utf8") as f:
    print(f.readlines())
```

## 如何写上下文管理器

想要自己实现一个类似于上面例子的上下文管理器,我们需要了解上下文管理器的组成部分,示例如下

```python
# 数据库连接类
class database_connect():
    def __enter__(self):
        print("数据库连接成功")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("断开数据库连接")

    def insert_data(self,a):
        print(f"插入数据:{a}")
        
# 使用方法
with database_connect() as db:
    db.insert_data(111)
    
# 输出结果
数据库连接成功
插入数据:111
断开数据库连接
```

1. `with` 上下文管理器中必须得有`__enter__` 和`__exit__` 这两个方法,`__enter__` 是执行方法的前提,也可以理解为入口,`__exit__` 是退出时要执行的操作

2. 除了这两个方法以外,`insert_data` 是我们实现的操作数据库的方法,我们可以根据实际情况编写多个,比如删除数据,查询数据等

3. 如何使用参考代码中的使用方法

4. 根据输出结果,我们可以看出他的执行顺序

   1. 是执行`__entry__()`进行数据库连接,返回数据库连接对象

   2. 利用数据库连接对象插入数据

   3. 数据插入后调用`__exit__()`断开数据库连接

## 上下文管理器一般的使用场景

   1. 数据库连接,可以自动关闭数据库连接
   2. 文件操作
   3. 网络连接 等等
