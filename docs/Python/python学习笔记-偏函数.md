# 偏函数
> 把一个函数的某些参数给固定住（也就是设置默认值），返回一个新的函数
```
import functools

# 获取天气
def get_weather(address="北京"):
    print(f"当前城市:{address}")
# 获取上海天气
get_weather(address="上海")
# 使用偏函数获取
get_weather2 = functools.partial(get_weather,address="上海")
get_weather2()
```