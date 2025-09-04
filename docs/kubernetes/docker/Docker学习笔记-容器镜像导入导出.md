# 镜像导入导出
## 导出镜像
```shell
docker save 镜像id > 镜像名称.tar
```
## 导入镜像
```shell
docker save < 镜像名称.tar
```
# 容器导入导出
## 导出容器
```shell
docker export 容器id > 容器名称.tar
```
## 导入镜像
```shell
docker import 容器名称.tar
```

