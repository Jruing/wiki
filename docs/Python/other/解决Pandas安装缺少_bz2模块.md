
## Centos 7 解决办法

```shell
yum install bzip2-devel
```
## Ubuntu 解决办法
```shell
sudo apt-get install libbz2-dev
```

##  重新编译Python3
> 需要先执行上面的命令安装bzip2

```shell
cd Python-3.6.5
# ./configure --enable-optimizations  # 不指定路径
./configure --prefix=/usr/local/python36 --enable-optimizations # 指定路径
sudo make && make install
```

