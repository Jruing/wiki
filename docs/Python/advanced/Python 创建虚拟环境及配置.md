# Python 创建虚拟环境及配置

## 介绍

https://docs.python.org/zh-cn/3/library/venv.html 官方文档

### 什么是python的虚拟环境

> 所谓的python虚拟环境，我们可以类比虚拟机的概念，每一个python虚拟环境都包含基本的python库，是能够独立运行的执行空间。在虚拟环境里可以下载第三方包、创建项目、写代码等等。因为虚拟环境之间互不干扰，一旦进入某个虚拟环境后，下载、安装的包，仅仅只会安装到该虚拟环境里。

### 为什么需要安装虚拟环境

> 假如我们有2个项目,A用的django 1.11版本,B用的django 3.x版本,如果我们只有一个python环境,那么我们是没办法同时运行这两个项目的,但是我们可以创建2个虚拟环境,一个装django 1.11版本,一个安装django3.0  通过不同的虚拟环境分别启动A和B这两个项目,还有一个好处就是当项目需要上线的时候,我们只需要把虚拟环境中的所有的第三方包导出来就可以了,不用担心多装或者少装第三方包

## 前提

环境:_windows 10_   _python 3.6.8_

## 安装

```
# 在当前路径下创建python虚拟环境
python -m venv venv_name #虚拟环境名称
```

 ## 使用

```
cd venv_name\Scripts
# 进入虚拟环境
activate
# 退出当前虚拟环境
deactivate
# 安装第三方包(必须进入虚拟环境)
pip install xxx
```

## 配置pip

```powershell
# 添加阿里云pypi镜像源
pip config set global.index-url  http://mirrors.aliyun.com/pypi/simple
# 因为阿里云pypi是http的,所以需要加上下面一行,https可以忽略
pip config set global.trusted-host mirrors.aliyun.com
# 禁用pip版本检查
pip config set global.disable-pip-version-check true
# 配置超时时间
pip config set global.timeout 120
```

