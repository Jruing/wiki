# Python学习笔记-装饰器

> Python 中的装饰器（Decorator）是一种用于修改或扩展函数或方法行为的特殊函数，通常用于在不修改原函数代码的情况下，添加额外的功能，例如日志记录、权限检查、性能测试等

## 函数装饰器用法

> `decorator` 是一个装饰器函数，它接受一个函数 `func` 作为参数，并返回一个新的函数 `wrapper`。`wrapper` 函数通常会在调用 `func` 之前或之后执行一些额外的代码。

```
# 实现统计函数运行时间的装饰器
import time
# 定义装饰器函数
def decorator(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        print(f"开始时间:{start}")
        result = func(*args, **kwargs)
        end = time.time()
        print(f"结束时间:{end}")
        print("runtime:", end - start)
        return result
    return wrapper
    
# 调用装饰器
@decorator
def func01():
    print("func01")
    time.sleep(3)

func01()
```

## 带参数的装饰器用法

> `retry` 是一个可接收参数的装饰器

```
# 实现重试机制
import time

def retry(num):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"重试次数:{num}")
            for i in range(1,num+1):
                print("当前次数:",i)
                start = time.time()
                print(f"开始时间:{start}")
                func(*args, **kwargs)
                end = time.time()
                print(f"结束时间:{end}")
                print("runtime:", end - start)
        return wrapper
    return decorator

@retry(num=3)
def func01():
    print("func01")
    time.sleep(3)

func01()
```

## 类装饰器用法

> - 类装饰器是一个类，它通过实现 `__call__` 方法来模拟函数的行为。
> - 类装饰器通常接受一个函数作为参数，并在 `__call__` 方法中定义装饰逻辑。

```
# 限制函数调用次数
class MaxCallLimit:
    def __init__(self, max_calls):
        self.max_calls = max_calls  # 最大调用次数
        self.count = 0              # 初始化计数器

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if self.count >= self.max_calls:
                raise Exception(f"Function '{func.__name__}' has exceeded the maximum call limit of {self.max_calls}.")
            self.count += 1
            print(f"Function '{func.__name__}' has been called {self.count} times.")
            return func(*args, **kwargs)
        return wrapper

# 使用带参数的类装饰器
@MaxCallLimit(max_calls=2)
def say_hello(name):
    print(f"Hello, {name}!")

# 测试
say_hello("Alice")
say_hello("Bob")
say_hello("Charlie")  # 这里会抛出异常
```

