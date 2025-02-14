# Python学习笔记-Schema数据结构及类型校验

> 使用 `schema` 库来执行数据结构的校验。`schema` 是一个简单而强大的库，用于定义和验证 Python 数据结构的约束

## And

>`And` 代表必选，数据结构里必须包含这个 schema，如下方声明了 `name` ，则代表这个`name`必须存在与字典中

```python
from schema import Schema, And, SchemaError
user_schema = Schema([
    {
        "name": And(str)
    }
])
user_data_1 = [{
    "name": "jruing",
}]
user_data_2 = [{
    "name": 666,
}]
try:
    user_result_1 = user_schema.validate(user_data_1)
    print(f"数据校验user_result_1：{user_result_1}")
except SchemaError as e:
    print(f"数据校验异常user_result_1:{e}")

try:
    user_result_2 = user_schema.validate(user_data_2)
    print(f"数据校验user_result_2：{user_result_2}")
except SchemaError as e:
    print(f"数据校验异常user_result_2:{e}")
==========调用结果==========
数据校验user_result_1：[{'name': 'jruing'}]
数据校验异常user_result_2:Or({'name': And(<class 'str'>)}) did not validate {'name': 666}
Key 'name' error:
666 should be instance of 'str'
```

## Or

> `Or` 代表值的类型必须为某两个类型，比如`int` 或 `float`，`tuple`或`list`

```python
from schema import Schema, And, SchemaError, Or
user_schema = Schema([
    {
        "name": And(str),
        "money": Or(int,float)
    }
])
user_data_1 = [{
    "name": "jruing",
    "money": 1000,
}]
user_data_2 = [{
    "name": "jruing",
    "money": 1000.1,
}]
user_data_3 = [{
    "name": "jruing",
    "money": "1000.1",
}]
try:
    user_result_1 = user_schema.validate(user_data_1)
    print(f"数据校验user_result_1：{user_result_1}")
except SchemaError as e:
    print(f"数据校验异常user_result_1:{e}")

try:
    user_result_2 = user_schema.validate(user_data_2)
    print(f"数据校验user_result_2：{user_result_2}")
except SchemaError as e:
    print(f"数据校验异常user_result_2:{e}")

try:
    user_result_3 = user_schema.validate(user_data_3)
    print(f"数据校验user_result_3：{user_result_3}")
except SchemaError as e:
    print(f"数据校验异常user_result_3:{e}")
==========调用结果==========
数据校验user_result_1：[{'name': 'jruing', 'money': 1000, 'addr': '中国', 'country': '中国', 'email': '123456@qq.com'}]
数据校验异常user_result_2:Or({'name': And(<class 'str'>), 'money': Or(<class 'int'>, <class 'float'>), Optional('addr'): And(<class 'str'>), Optional('email'): And(<class 'str'>, Regex('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$', flags=re.IGNORECASE)), 'country': Const('中国')}) did not validate {'name': 'jruing', 'money': 1000.1, 'addr': '1111', 'country': '山西', 'email': '123456'}
Key 'country' error:
'中国' does not match '山西'
```



## Const

> `Const` 代表值必须为指定的某个常量，比如下面的 `country`必须为`中国`

```
import re

from schema import Schema, And, SchemaError, Or, Optional, Regex, Const

user_schema = Schema([
    {
        "name": And(str),
        "money": Or(int, float),
        Optional("addr"): And(str),
        Optional("email"): And(str, Regex(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', flags=re.I)),
        "country": Const("中国")

    }
])
user_data_1 = [{
    "name": "jruing",
    "money": 1000,
    "addr": "中国",
    "country": "中国",
    "email": "123456@qq.com"

}]
user_data_2 = [{
    "name": "jruing",
    "money": 1000.1,
    "addr": "1111",
    "country": "山西",
    "email": "123456"

}]

try:
    user_result_1 = user_schema.validate(user_data_1)
    print(f"数据校验user_result_1：{user_result_1}")
except SchemaError as e:
    print(f"数据校验异常user_result_1:{e}")

try:
    user_result_2 = user_schema.validate(user_data_2)
    print(f"数据校验user_result_2：{user_result_2}")
except SchemaError as e:
    print(f"数据校验异常user_result_2:{e}")
==========调用结果==========
数据校验user_result_1：[{'name': 'jruing', 'money': 1000, 'addr': '中国', 'country': '中国', 'email': '123456@qq.com'}]
数据校验异常user_result_2:Or({'name': And(<class 'str'>), 'money': Or(<class 'int'>, <class 'float'>), Optional('addr'): And(<class 'str'>), Optional('email'): And(<class 'str'>, Regex('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$', flags=re.IGNORECASE)), 'country': Const('中国')}) did not validate {'name': 'jruing', 'money': 1000.1, 'addr': '1111', 'country': '山西', 'email': '123456'}
Key 'country' error:
'中国' does not match '山西'
```



## Optional

> `Optional` 代表这个key或者元素为非必选，可有可无

```
from schema import Schema, And, SchemaError, Or, Optional

user_schema = Schema([
    {
        "name": And(str),
        "money": Or(int, float),
        Optional("addr"): And(str)

    }
])
user_data_1 = [{
    "name": "jruing",
    "money": 1000,
    "addr": "中国"

}]
user_data_2 = [{
    "name": "jruing",
    "money": 1000.1,

}]

try:
    user_result_1 = user_schema.validate(user_data_1)
    print(f"数据校验user_result_1：{user_result_1}")
except SchemaError as e:
    print(f"数据校验异常user_result_1:{e}")

try:
    user_result_2 = user_schema.validate(user_data_2)
    print(f"数据校验user_result_2：{user_result_2}")
except SchemaError as e:
    print(f"数据校验异常user_result_2:{e}")
==========调用结果==========
数据校验user_result_1：[{'name': 'jruing', 'money': 1000, 'addr': '中国'}]
数据校验user_result_2：[{'name': 'jruing', 'money': 1000.1}]
```



## Use

>`Use` 函数允许你在验证前对数据进行转换。这对于在验证之前对数据进行清理、格式化或其他操作非常有用。

```
import re

from schema import Schema, And, SchemaError, Or, Optional, Regex, Const, Use

user_schema = Schema([
    {
        "name": And(str),
        "money": Or(int, float),
        "age": Use(int),
        Optional("addr"): And(str),
        Optional("email"): And(str, Regex(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', flags=re.I)),
        Optional("country"): Const("中国")

    }
])
user_data_1 = [{
    "name": "jruing",
    "money": 1000,
    "age": 11,
    "addr": "中国",
    "country": "中国",
    "email": "123456@qq.com"

}]
user_data_2 = [{
    "name": "jruing",
    "money": 1000.1,
    "age": "18",
    "addr": "1111",
    "email": "123456@qq.com"

}]
user_data_3 = [{
    "name": "jruing",
    "money": 1000.1,
    "age": "fff",
    "addr": "1111",
    "email": "123456@qq.com"

}]
try:
    user_result_1 = user_schema.validate(user_data_1)
    print(f"数据校验user_result_1：{user_result_1}")
except SchemaError as e:
    print(f"数据校验异常user_result_1:{e}")

try:
    user_result_2 = user_schema.validate(user_data_2)
    print(f"数据校验user_result_2：{user_result_2}")
except SchemaError as e:
    print(f"数据校验异常user_result_2:{e}")
try:
    user_result_3 = user_schema.validate(user_data_3)
    print(f"数据校验user_result_3：{user_result_3}")
except SchemaError as e:
    print(f"数据校验异常user_result_3:{e}")
==========调用结果==========
数据校验user_result_1：[{'name': 'jruing', 'money': 1000, 'age': 11, 'addr': '中国', 'country': '中国', 'email': '123456@qq.com'}]
数据校验user_result_2：[{'name': 'jruing', 'money': 1000.1, 'age': 18, 'addr': '1111', 'email': '123456@qq.com'}]
数据校验异常user_result_3:Or({'name': And(<class 'str'>), 'money': Or(<class 'int'>, <class 'float'>), 'age': Use(<class 'int'>), Optional('addr'): And(<class 'str'>), Optional('email'): And(<class 'str'>, Regex('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$', flags=re.IGNORECASE)), Optional('country'): Const('中国')}) did not validate {'name': 'jruing', 'money': 1000.1, 'age': 'fff', 'addr': '1111', 'email': '123456@qq.com'}
Key 'age' error:
int('fff') raised ValueError("invalid literal for int() with base 10: 'fff'")
```



## Regex

> 通过正则表达式，对值进行匹配校验，常用的就是邮箱，手机号等场景

```
import re

from schema import Schema, And, SchemaError, Or, Optional, Regex

user_schema = Schema([
    {
        "name": And(str),
        "money": Or(int, float),
        Optional("addr"): And(str),
        Optional("email"): And(str, Regex(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', flags=re.I))

    }
])
user_data_1 = [{
    "name": "jruing",
    "money": 1000,
    "addr": "中国",
    "email": "123456@qq.com"

}]
user_data_2 = [{
    "name": "jruing",
    "money": 1000.1,
    "addr": "1111",
    "email": "123456"

}]

try:
    user_result_1 = user_schema.validate(user_data_1)
    print(f"数据校验user_result_1：{user_result_1}")
except SchemaError as e:
    print(f"数据校验异常user_result_1:{e}")

try:
    user_result_2 = user_schema.validate(user_data_2)
    print(f"数据校验user_result_2：{user_result_2}")
except SchemaError as e:
    print(f"数据校验异常user_result_2:{e}")
==========调用结果==========
数据校验user_result_1：[{'name': 'jruing', 'money': 1000, 'addr': '中国', 'email': '123456@qq.com'}]
数据校验异常user_result_2:Or({'name': And(<class 'str'>), 'money': Or(<class 'int'>, <class 'float'>), Optional('addr'): And(<class 'str'>), Optional('email'): And(<class 'str'>, Regex('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$', flags=re.IGNORECASE))}) did not validate {'name': 'jruing', 'money': 1000.1, 'addr': '1111', 'email': '123456'}
Key 'email' error:
Regex('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$', flags=re.IGNORECASE) does not match '123456'
```



## Forbidden

> `Forbidder` 允许你定义一些不被允许的值，如果数据中包含这些值，验证将失败，下面的例子表示密码 `password`字段的值不允许设置为`123456`

```
import re

from schema import Schema, And, SchemaError, Or, Optional, Regex, Const, Use, Forbidden

user_schema = Schema([
    {
        "name": And(str),
        "money": Or(int, float),
        "age": Use(int),
        Optional("addr"): And(str),
        Optional("email"): And(str, Regex(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', flags=re.I)),
        Optional("country"): Const("中国"),
        "password": And(str, Forbidden("123456"))

    }
])
user_data_1 = [{
    "name": "jruing",
    "money": 1000,
    "age": 11,
    "addr": "中国",
    "country": "中国",
    "email": "123456@qq.com",
    "password": "123456"

}]
user_data_2 = [{
    "name": "jruing",
    "money": 1000.1,
    "age": "18",
    "addr": "1111",
    "email": "123456@qq.com",
    "password": "1234561"

}]

try:
    user_result_1 = user_schema.validate(user_data_1)
    print(f"数据校验user_result_1：{user_result_1}")
except SchemaError as e:
    print(f"数据校验异常user_result_1:{e}")

try:
    user_result_2 = user_schema.validate(user_data_2)
    print(f"数据校验user_result_2：{user_result_2}")
except SchemaError as e:
    print(f"数据校验异常user_result_2:{e}")
    
==========调用结果==========    
数据校验user_result_1：[{'name': 'jruing', 'money': 1000, 'age': 11, 'addr': '中国', 'country': '中国', 'email': '123456@qq.com', 'password': '123456'}]
数据校验异常user_result_2:Or({'name': And(<class 'str'>), 'money': Or(<class 'int'>, <class 'float'>), 'age': Use(<class 'int'>), Optional('addr'): And(<class 'str'>), Optional('email'): And(<class 'str'>, Regex('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$', flags=re.IGNORECASE)), Optional('country'): Const('中国'), 'password': And(<class 'str'>, Forbidden('123456'))}) did not validate {'name': 'jruing', 'money': 1000.1, 'age': '18', 'addr': '1111', 'email': '123456@qq.com', 'password': '1234561'}
Key 'password' error:
'123456' does not match '1234561'
```

