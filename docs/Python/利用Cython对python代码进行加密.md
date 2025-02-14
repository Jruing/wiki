# 利用Cython对python代码进行加密

> Cython是属于PYTHON的超集，他首先会将PYTHON代码转化成C语言代码，然后通过c编译器生成可执行文件。优势：资源丰富，适合快速开发。翻译成C后速度比较快，在windows环境中用cython加密后的文件后缀是pyd文件，在linux环境中加密后的问题后缀是so文件，下面以linux环境作为演示

## 环境准备

> 系统环境：centos 7
>
> Python版本：python3.x
>
> 需要的第三方包：cython

## 加密代码部分
encryption.py

```python
from distutils.core import setup
from Cython.Build import cythonize
setup(ext_modules = cythonize(["Jruing.py"]))  # 列表中是要加密的文件名
```

## 要加密的代码部分
Jruing.py
```
def hello_world():
    print("hello world！！！")
```
> 将以上代码保存为encryption.py，在命令行中输入python encryption.py build_ext，它会在encryption.py这个文件的当前路径下生成build文件夹，build/lib-\*/Jruing-\*.so （“*”部分代表的是Python版本等一系列信息，这个不重要，windows环境会在同样的目录下生成Jruing-\*.pyd文件），我们可以把这个so文件直接重命名为Jruing.so

## 调用加密后的文件中的函数
我们进入到so文件所在的目录，编写一个调用hello_world的程序

```python
from Jruing import hello_world # Jruing为so文件的文件名
hello_world()
```

## 加密Flask Web服务

> flask 文件一般会创建一个app对象，它启动也是通过这个app对象去启动的，直接加密会加密成功，但是执行会出现问题，我们可以在调用文件中导入app对象，然后app.run()启动就可以了，具体操作如下

### 一个flask web服务Demo
flask_demo.py
```
from flask import Flask
app = Flask(__name__)

@app.route('/',methods=['GET'])
def root():
    return "hello world"
if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)
```
在加密之前我们把它改为
flask_demo_test.py
```
from flask import Flask
app = Flask(__name__)

@app.route('/',methods=['GET'])
def root():
    return "hello world"
```
用上面提到的方法对flask_demo_test.py文件进行加密
### 调用flask_demo_test.py启动服务
```
from flask_demo_test import app
app.run(host='127.0.0.1',port=5000)
```
这样就好了！！！！

