# Frp 内网穿透搭建

## 简介

> - frp 是一个专注于内网穿透的高性能的反向代理应用，支持 TCP、UDP、HTTP、HTTPS 等多种协议。
> - 可以将内网服务以安全、便捷的方式通过具有公网 IP 节点的中转暴露到公网。

## 下载地址

> https://github.com/fatedier/frp/releases/tag/v0.61.1

### 服务端配置文件

```toml
# frps.toml
bindPort = 7000                         # 服务端与客户端通信端口

transport.tls.force = true              # 服务端将只接受 TLS链接

auth.token = "public"                   # 身份验证令牌，frpc要与frps一致

# Server Dashboard，可以查看frp服务状态以及统计信息
webServer.addr = "0.0.0.0"              # 后台管理地址
webServer.port = 7500                   # 后台管理端口
webServer.user = "admin"                # 后台登录用户名
webServer.password = "admin"            # 后台登录密码
```

### 启动服务端

```
./frps -c frps.toml
```

### 客户端配置文件

```
# frpc.toml
serverAddr = "1.1.1.1" # 服务端ip
serverPort = 7000      # 服务端端口
auth.token= "public"   # 服务端配置的token信息
[[proxies]]
name = "test-tcp"      # 服务名称自定义
type = "tcp"           # 通信协议类型
localIP = "127.0.0.1"  # 本地服务ip
localPort = 8000       # 本地服务端口
remotePort = 8081      # 外网访问端口,建议选择大于8000的端口
```

### 启动客户端

```
./frpc -c frpc.toml
```

### 后台管理页面

![image-20241218104053060](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20241218104053060.png)
