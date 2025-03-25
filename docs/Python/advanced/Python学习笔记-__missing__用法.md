# Python学习笔记- __missing__用法

## `__missing__` 方法的作用

- `__missing__` 方法在字典的子类中定义，当通过 `dict[key]` 访问一个不存在的键时，如果定义了 `__missing__` 方法，Python 会自动调用它。
- 这个方法允许你自定义字典在键不存在时的行为，而不是直接抛出 `KeyError`。

## 自定义默认值

> 当访问一个不存在的key时，则会返回指定的默认值，不会返回`KeyError`异常

```
class DefaultDict(dict):
    def __missing__(self, key):
        return None

# 创建自定义字典
my_dict = DefaultDict({'a': 1, 'b': 2})

# 访问存在的键
print(my_dict['a'])  # 输出: 1

# 访问不存在的键
print(my_dict['c'])  # 输出: None
```

## 注意事项

- `__missing__` 方法仅在通过 `dict[key]` 访问键时生效。如果使用 `dict.get(key)` 方法，`__missing__` 不会被调用。
- `__missing__` 方法只能在字典的子类中定义，不能直接用于普通的 `dict` 对象

