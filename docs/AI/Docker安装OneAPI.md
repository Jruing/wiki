## Docker部署安装
```
docker volume create oneapi
docker run --name oneapi -d --restart=always -p 3000:3000 -e TZ=Asia/Shanghai -v oneapi:/data justsong/one-api:latest
```
## 访问地址
> http://ip:3000


## 默认账号密码
> root/123456

## 创建渠道

![image-20250313173546822](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250313173546822.png)

## 创建令牌

![image-20250313173651383](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250313173651383.png)

![image-20250313173747444](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250313173747444.png)

## API调用

> Base URL:http://ip:3000
>
> API key: 上面的令牌
