# Python 读取指定文件指定行
## 场景
读取配置文件中指定行,根据读取的值判断后续的逻辑
## 解决方案
> 采用python内置的包`linecache`
```
import linecache
content = linecache.getline(filename=r'test01.txt',lineno=1)
content1 = linecache.getlines('test01.txt')
```

## 源码
`getline`方法的源码如下
```
def getline(filename, lineno, module_globals=None):
    lines = getlines(filename, module_globals)
    if 1 <= lineno <= len(lines):
        return lines[lineno-1]
    else:
        return ''
```

`getlines`方法的源码如下
```
def getlines(filename, module_globals=None):
    """Get the lines for a Python source file from the cache.
    Update the cache if it doesn't contain an entry for this file already."""

    if filename in cache:
        entry = cache[filename]
        if len(entry) != 1:
            return cache[filename][2]

    try:
        return updatecache(filename, module_globals)
    except MemoryError:
        clearcache()
        return []

```

`getlines`是将文件内容按行转换成列表,`getline`从`getlines`返回的列表中根据下表取出相应的内容
