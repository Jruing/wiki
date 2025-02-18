# Docker Swarm 学习笔记

## 初始化集群

```
docker swarm init
```

> 若机器有多个ip，则需要在后面加上 `--advertise-addr ip地址` 指定ip ,执行该命令后该节点自动成为管理节点

## 增加工作节点

```
docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377
```

## 查询集群节点

```
docker node ls
```

## 部署服务

```
docker service create --replicas 3 -p 8080:80 -p 8081:80 -p:8082  --name nginx nginx:html
```

> 此处创建了一个名称为nginx，端口为80，3个副本的nginx服务

## 查看服务列表

```
docker service ls
```

## 查看服务详情

```
docker service ps 服务名称或id
```

## 查看服务日志

```
docker service logs 服务名称或id
```

## 服务扩缩容

```
docker service scale nginx=5
```

> 将nginx服务扩充到5个节点

## 删除某个服务

```
docker service rm 服务名称或服务id
```

## 服务滚动升级

```
docker service update --image nginx:latest nginx 
```

## 服务回退

```
docker server rollback nginx
```

