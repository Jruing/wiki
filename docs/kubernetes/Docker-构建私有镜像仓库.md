# 前置条件

```
# 修改/etc/docker/daemon.json
{
    "registry-mirrors": [
        "https://mirror.ccs.tencentyun.com"
    ],
    "insecure-registries":["192.168.1.233:8080"] # 镜像仓库地址
}
# 重载
systemctl daemon-reload
# 重启docker
systemctl restart docker
```
# 方式一（不推荐）
## 创建一个数据卷
```
docker volume create registry_volumn
```
## 启动服务
```
docker run -d \
    --restart=always \
    --name registry	\
    -p 5000:5000 \
    -v registry_volumn:/var/lib/registry \
    registry
```
# 方式二(推荐)
## docker-compose.yml
```
version: '3.0'
services:
  registry:
    image: registry
    volumes:
      - registry_volumn:/var/lib/registry
  ui:
    image: joxit/docker-registry-ui:static
    ports:
      - 8080:80
    environment:
      - REGISTRY_TITLE=Jruing的私有镜像仓库
      - REGISTRY_URL=http://registry:5000
      - CATALOG_ELEMENTS_LIMIT=1000
    depends_on:
      - registry
volumes:
  registry_volumn:  
```
## 启动
```
docker-compose up -d
```
# 页面
> http://192.168.1.233:8080
# 测试

```
docker tag nginx:latest 192.168.1.233:8080/nginx:1.0
```
## 推送
```
docker push 192.168.1.233:8080/nginx:1.0
```
## 拉取
```
docker pull 192.168.1.233:8080/nginx:1.0
```
## 预览页面

![image-20250312171220502](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250312171220502.png)
