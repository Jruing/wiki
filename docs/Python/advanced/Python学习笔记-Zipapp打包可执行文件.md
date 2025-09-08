> 使用场景：只需要项目所需指定版本的Python解释器就可以运行由zipapp打包后的项目
>
> 环境要求
>
> ​	打包方：需要有项目及项目所依赖的所有开发环境（Python解释器，第三方库）
>
> ​	使用方：需要有项目所需指定版本的Python解释器
>
> 官方文档：https://docs.python.org/zh-cn/3/library/zipapp.html#zipapp-specifying-the-interpreter

## 概念

> zipapp会将项目打包为一个独立的可执行文件，可在任何装有合适解释器的机器上运行

## 例子

1. 创建目录 `myapp`

2. 下载依赖到`myapp`目录中

```
python -m pip install flask --target myapp
```

3. 创建文件 `testapp.py`，将文件放入`myapp`目录中

```
# encoding:utf8

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
      return "Hello World!"

def main():
      app.run()
```

4. 打包

```
# 方式一
# 参数解释
# -o 输出文件名称，文件名称必须有pyz后缀
# -c 利用 deflate 方法压缩文件，减少输出文件的大小，默认不压缩
# -m 指定调用对象，模块中的方法mod:function，如果是多层级，则是pkg.mod:function
# -p 指定解释器，尽量避免使用具体版本的Python解释器，如python3.6，若打包的可执行文件需要在liunx中执行，则必须指定，参考 `/usr/bin/python`
python -m zipapp myapp -o app.pyz -c -m "testapp:main"

# 方式二
import zipapp
zipapp.create_archive('myapp', 'app.pyz')
```

5. 运行方式

```
# 方式一
python app.pyz
# 方式二
在配置python解释器环境变量后，windows上可以直接双击运行
```

## 注意事项

如果应用程序依赖某个带有 C 扩展的包，则此程序包无法由打包文件运行（这是操作系统的限制，因为可执行代码必须存在于文件系统中，操作系统才能加载）。这时可去除打包文件中的依赖关系，然后要求用户事先安装好该程序包，或者与打包文件一起发布并在 `__main__.py` 中增加代码，将未打包模块的目录加入 `sys.path` 中。采用增加代码方式时，一定要为目标架构提供合适的二进制文件（可能还需在运行时根据用户的机器选择正确的版本加入 `sys.path`）。

## 总结

zipapp 在部分场景下降低了项目迁移及运行的难度，适合在有合适解释器的大部分机器上使用
