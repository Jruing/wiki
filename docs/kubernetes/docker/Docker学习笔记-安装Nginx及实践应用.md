> 本文以下面链接文件为测试过程，为了方便，可以在本地把文件解压后重新压缩为 zip类型的压缩包
> [http://www.mobanwang.com/mb/UploadFiles_2010/lo202105/202105033.rar](http://www.mobanwang.com/mb/UploadFiles_2010/lo202105/202105033.rar)

# 拉取镜像
```yaml
[root@VM-24-9-centos ~]# docker pull nginx
Using default tag: latest
latest: Pulling from library/nginx
8740c948ffd4: Pull complete 
d2c0556a17c5: Pull complete 
c8b9881f2c6a: Pull complete 
693c3ffa8f43: Pull complete 
8316c5e80e6d: Pull complete 
b2fe3577faa4: Pull complete 
Digest: sha256:b8f2383a95879e1ae064940d9a200f67a6c79e710ed82ac42263397367e7cc4e
Status: Downloaded newer image for nginx:latest
docker.io/library/nginx:latest
```
# 创建映射目录
```yaml
# 创建Nginx静态页面文件目录
mkdir -p /usr/local/src/docker_nginx/html
# 创建Nginx配置文件目录
mkdir -p /usr/local/src/docker_nginx/conf
```
# 上传html静态页面Demo
```yaml
# 要上传到上面新建的静态页面文件目录中
cd /usr/local/src/docker_nginx/html

# 解压文件
unzip 202105033.zip

# 将202105033/html中的所有文件移动到当前路径下
mv 202105033/html/* ./
```
# 修改Nginx配置文件
```yaml

#user  nobody;
worker_processes  1;

#error_log  /var/logerror.log;
#error_log  /var/logerror.log  notice;
#error_log  /var/logerror.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    # access_log  /var/log/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    gzip  on;

    server {
        # 监听 80 端口
        listen       80;
        server_name  localhost;
        location / {
            # nginx静态页面在docker中存放的路径
            root   /usr/share/nginx/html;
            index  index.html index.htm;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }

}

```
# 启动镜像
```yaml
docker run -p 80:80 --name nginx \
-v /usr/local/src/docker_nginx/html:/usr/share/nginx/html \
-v /usr/local/src/docker_nginx/conf:/etc/nginx/nginx.conf \
-itd a99a39d070bf
# -p 为端口映射，将容器的80端口映射到宿主机的80端口
# 上面-v部分冒号前面的内容需要替换为上面新建的映射目录，结尾为nginx镜像ID（可以通过docker images查询）

```
# 展示效果
> 访问地址：http://localhost

![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/docker_nginx_1.png)

