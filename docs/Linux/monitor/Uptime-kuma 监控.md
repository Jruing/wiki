
> 简介
>
> - 监控 HTTP（s） / TCP / HTTP（s） 关键字 / HTTP（s） Json 查询 / Ping / DNS 记录 / 推送 / Steam 游戏服务器 / Docker 容器的正常运行时间
> - 通过 Telegram、Discord、Gotify、Slack、Pushover、电子邮件 （SMTP） 和 [90+ 通知服务发送通知](https://github.com/louislam/uptime-kuma/tree/master/src/components/notifications)

## 准备工作

* Centos 7
* docker-ce

## 安装

```
docker pull louislam/uptime-kuma:1
docker run -d --restart=always -p 3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:1
```

## 配置

> 访问 http://ip:3001

### 基础配置

![image-20240707132251308](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202407071323787.png)

![image-20240707132546465](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202407071325624.png)

### 监控详情页面

![image-20240707132740684](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202407071327834.png)

### 监控项状态页面

![image-20240707132905795](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202407071329938.png)

![image-20240707133003955](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202407071330113.png)

![](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202407071334949.png)

![image-20240707133514317](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202407071335428.png)

### 配置维护信息

> 右上角`我的`->`维护`

![image-20240707134212811](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202407071342933.png)

![image-20240707134000732](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202407071340862.png)
