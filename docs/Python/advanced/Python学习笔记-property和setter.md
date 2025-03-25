# Python学习笔记-property和setter

## property装饰器

> 将类的方法转换为只读属性，允许你像访问属性一样调用方法，而不需要使用括号。

```python
@property
def sorce(self):
    # 方法体
    pass
```

## setter装饰器

> 为 `property` 属性提供设置值的功能，允许你定义如何设置属性的值。

```python
@sorce.setter
def sorce(self, value):
    # 设置逻辑
    pass
```

## 栗子

```python
# encoding:utf8

class Student:
    def __init__(self, name, score):
        self.name = name
        self._score = score
    
    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError("score must be an integer!")
        if value < 0 or value > 100:
            raise ValueError("score must between 0~100!")
        self._score = value
if __name__ == '__main__':
    b = Student('Bob', 59)
    # 可以像访问属性一样调用score方法
    print(b.score)
    # 设置属性_score的值
    b.score = 600
    print(b.score)
```

## 注意

> 如果只声明了`property` 装饰器，没有声明`setter`装饰器 ，在实例化之后手动修改属性值的时候则会出现以下异常：
>
> AttributeError: property 'score' of 'Student' object has no sette