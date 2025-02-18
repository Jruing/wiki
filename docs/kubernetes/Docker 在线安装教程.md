
## 环境准备

Centos 7.6（可以连接公网）

## 步骤

### 更新yum
```
yum update
```

### 安装工具包
```
yum -y install yum-utils
```

### 设置yum源(以阿里云镜像源为例)
```
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
# 腾讯
https://mirrors.cloud.tencent.com/docker-ce/linux/centos/docker-ce.repo
```

### 安装Docker-Ce(社区版)
```
yum -y install docker-ce
```

### 查看docker版本（用来确认是否安装成功）
```
# 输入 docker-v 后如果出现下面的内容则代表安装成功
[root@VM-24-9-centos ~]# docker -v
Docker version 20.10.23, build 7155243
```

### Docker镜像加速（国内使用）
```
# 需要确定/etc下面是否有docker这个文件夹，若没有则需要使用下面的命令进行创建
mkdir -p /etc/docker

# 创建配置文件daemon.json
touch /etc/docker/daemon.json

# 写入以下内容
{
   "registry-mirrors": [
         "https://mirror.ccs.tencentyun.com" # 可以替换为其他厂商的地址
   ]
}
```
### 重载配置
```
systemctl daemon-reload
```

### 启动Docker服务
```
systemctl start docker
```

### 验证docker是否可以使用
```
[root@VM-24-9-centos ~]# docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

   