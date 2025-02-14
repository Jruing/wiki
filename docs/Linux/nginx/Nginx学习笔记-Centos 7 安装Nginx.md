
[toc]

## 前置条件

### 安装GCC

```
yum install -y gcc-c++
```

### 安装pcre

```
yum install -y pcre pcre-devel
```

### 安装zlib

```
yum install -y zlib zlib-devel
```

### 安装openssh

```
yum install -y openssl openssl-devel
```

## 安装Nginx
### 下载Nginx

> 官网：https://nginx.org/en/download.html

```
curl -o /usr/local/src/Nginx/nginx-1.23.4.tar.gz https://nginx.org/download/nginx-1.23.4.tar.gz
```

### 解压&编译安装

```
# 进入目录
cd /usr/local/src/Nginx/nginx-1.23.4
# 编译
./configure --prefix=/usr/local
# 安装
make & make install
```

### 常用命令

```
# 查看帮助信息
nginx -h

# 查看nginx版本
nginx -v

# 启动nginx
nginx -c filename(配置文件名称及路径)

# 停止nginx
nginx -s quit(平滑停止) / nginx -s stop（立即停止）

# 重载nginx配置文件
nginx -s reload

#  检查配置文件是否正确
nginx -t -c filename（配置文件名称及路径）
```
### Nginx安装其他模块
> 以`ngx_http_stub_status_module`为例,在编译时需要加上该模块,https://nginx.org/en/docs/http/ngx_http_stub_status_module.html
```
# 进入目录
cd /usr/local/src/Nginx/nginx-1.23.4
# 编译
./configure --prefix=/usr/local --with-http_stub_status_module
# 安装
make & make install
```
