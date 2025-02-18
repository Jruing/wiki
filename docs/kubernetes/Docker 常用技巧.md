# 常用技巧
## 临时性容器
> 运行一个容器，执行特定任务后自动退出，并且不会保留容器的状态。这种容器通常用于临时任务，如运行脚本、测试代码或执行命令。

```
docker run -it --rm ubuntu:latest /bin/bash
```

## 删除所有容器
```
docker rm -f $(docker ps -aq)
```
