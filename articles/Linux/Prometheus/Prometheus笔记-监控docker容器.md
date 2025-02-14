# docker安装google/cadvisor
```
[root@VM-24-9-centos ~]# docker pull google/cadvisor
Using default tag: latest
latest: Pulling from google/cadvisor
ff3a5c916c92: Pull complete 
44a45bb65cdf: Pull complete 
0bbe1a2fe2a6: Pull complete 
Digest: sha256:815386ebbe9a3490f38785ab11bda34ec8dacf4634af77b8912832d4f85dca04
Status: Downloaded newer image for google/cadvisor:latest
docker.io/google/cadvisor:latest
```
# 启动cadvisor容器
```
docker run -d \
--volume=/:/rootfs:ro \
--volume=/var/run:/var/run:rw \
--volume=/sys:/sys:ro \
--volume=/var/lib/docker/:/var/lib/docker:ro \
--publish=8080:8080 \
--detach=true \
--name=cadvisor \
-v "/etc/localtime:/etc/localtime" \
google/cadvisor:latest
```
# cadvisor页面展示
> 访问地址 http://ip:8080

![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/prometheus_docker_cadvisor_1.png)
# 添加Prometheus子配置文件
```yaml
# 子配置文件名称为docker_exporter.yml
- targets: ['localhost:58080']
  labels:
    env: 'test'
    host: 'localhost'
    type: 'docker_exporter'
```
# Prometheus配置文件新增job_name
```yaml
- job_name: "docker_exporter"
    metrics_path: '/metrics'
    scheme: 'http'
    file_sd_configs:
      # 子配置文件路径需要改为自己的
      - files: ["/usr/local/src/Prometheus_server/prometheus-2.41.0.linux-amd64/child_config/docker_exporter.yml"]
```
# Prometheus 显示效果
![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/prometheus_docker_cadvisor_2.png)
