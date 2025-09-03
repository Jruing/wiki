# Ubuntu 22.04 上安装 Python 3.12 

### 1. 更新系统包索引

首先确保系统的包索引是最新的：

```
sudo apt update
sudo apt upgrade -y
```

### 2. 安装依赖包

安装编译 Python 所需的依赖包：

```
sudo apt install -y build-essential zlib1g-dev libncurses5-dev \
libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget
```

### 3. 下载 Python 3.12 源码

从 Python 官方网站下载 Python 3.12 的源码包：

```
wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
```

### 4. 解压并编译源码

解压下载的源码包并进入目录：

```
tar -xf Python-3.12.0.tgz
cd Python-3.12.0
```

配置编译选项并编译安装：

```
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall
```

--enable-optimizations 选项会启用优化编译，提高 Python 的运行速度。

make altinstall 避免覆盖系统默认的 Python 版本。

### 5. 验证安装

安装完成后，验证 Python 3.12 是否正确安装：

```
python3.12 --version
```

输出应为：Python 3.12.0

### 6. 可选：设置为默认 Python 版本

如果需要将 Python 3.12 设置为默认版本，可以使用以下命令：

```
sudo update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.12 1
```

然后通过以下命令选择默认版本：

```
sudo update-alternatives --config python3
```

### 7. 安装 pip

Python 3.12 通常会自带 pip，但如果需要单独安装：

```
sudo apt install -y python3.12-distutils
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.12 get-pip.py
```

完成以上步骤后，你就可以在 Ubuntu 22.04 上使用 Python 3.12 了。