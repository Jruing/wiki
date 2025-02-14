> 在Python 3.5版本之前是没有参数类型提示的,在3.5版本加入了这一项,这一项新的内容的优点在于帮助我们明确函数中每个参数的类型是什么,方便排查问题及项目交接后,下一任能够看懂代码,但是这一样不像其他语言一样强制检查参数类型,这里只是为了提示,不影响代码执行
> 具体文档参考官网文档: [https://docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html)


---

## 不加入类型提示
```python
from typing import List

def say(msg):
    """
    msg: 消息
    """
    return msg
```
## 加入类型提示后
```python
from typing import List # 需要导入 typing 包

# 单条消息
def say(msg:str) -> str: # -> 函数返回值的类型
    """
    msg: 消息
    """
    return msg
# 多条消息  
def say(msg:List) -> List: # -> 函数返回值的类型
    """
    msg: 消息
    """
    return msg
```
我们先看下不加入类型提示的代码,因为它所需要的参数 `msg` 没有类型注释,这个函数的返回值也没有类型注释,这样的话我们虽然可以正确执行,但是在理解的时候虽然知道他接收的是`msg`, 但是不知道这个是一条消息,还是多条消息,而我们在加入类型提示后,我们就知道这里接收的是单条消息,还是一个消息列表.
​

## 常用参数类型
### Str 字符型
```python
# 单条消息
def say(msg:str) -> str: # -> 函数返回值的类型
    """
    msg: 消息
    """
    return msg

say("hello world") # 支持
say(111) # 不支持
```
### Int 整型
```python
# 单条消息
def say(stuid:id) -> id: # -> 函数返回值的类型
    """
    stuid: 学生id
    """
    return stuid

say(20210001)
```
### Float 浮点型
```python
# 单条消息
def say(pi:float) -> float: # -> 函数返回值的类型
    """
    pi: Π,3.1415926
    """
    return pi

say(3.14)
```
### Bool 布尔型
```python
# 单条消息
def say(is_win:bool) -> bool: # -> 函数返回值的类型
    """
    is_win: 是否赢了
    """
    return pi

say(True)
```
### List 列表
```python
# 多条消息  
def say(msg:List) -> List: # -> 函数返回值的类型
    """
    msg: 消息
    """
    return msg

say(["hello","world"])
```
### Tuple 元组
```python
# 多条消息  
def say(stuid:Tuple) -> Tuple: # -> 函数返回值的类型
    """
    stuid: 学生id
    """
    return msg

say((2021001,2021002,2021003,))
```
### Dict 字典
```python
# 单条消息
def say(stuinfo:Dict) -> Dict: # -> 函数返回值的类型
    """
    stuinfo: 学生信息
    """
    return stuinfo

say({"stu_name":"张三"})
```
### New Type 自定义类型
```python
from typing import NewType
UserName = NewType('UserName',str) 
def say(name:UserName) -> UserName:# -> 函数返回值的类型
    """
    name: 名字
    """
    return name

say("张三") # 支持
say(111) # 不支持
```
### Union 公用类型
```python
from typing import Union
# Union[int,List] 支持int类型或者List类型,不支持其他类型的参数
def say(msg:Union[int,List]) -> Union[int,List]:# -> 函数返回值的类型
    """
    msg: 消息
    """
    return msg

say("hello") # 不支持(类型检查不支持,不影响代码执行)
say([111,222]) # 支持
say(111) # 支持
```
### Optional
```python
from typing import Optional
# Optional[str] 是对于存在默认的情况,若有默认值,则采用默认值,否则采用str类型
def say(msg:Optional[str]=None) -> None:# -> 函数返回值的类型
    """
    msg: 消息
    """
    return msg

say("hello") # 支持
say() # 支持
say(111) # 不支持
```
### 复合类型
```python
MsgType = List[str] # 声明一个列表套字符串的类型,例如:["hello"]
def say(msg:MsgType) -> List:# -> 函数返回值的类型
    """
    msg: 消息
    """
    return msg

say(["hello","world"]) # 支持
say([111,222]) # 不支持
say(111) # 不支持
```

