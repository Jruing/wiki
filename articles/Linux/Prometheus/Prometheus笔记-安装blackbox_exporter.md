> Blackbox Exporter是Prometheus社区提供的官方黑盒监控解决方案，其允许用户通过：HTTP、HTTPS、DNS、TCP以及ICMP	的方式对网络进行探测。我们可以利用这个exporter定时访问业务系统某个接口来确定服务是否存活


# 下载
```yaml
[root@VM-24-9-centos exporter_package]# wget https://ghproxy.com/https://github.com/prometheus/blackbox_exporter/releases/download/v0.23.0/blackbox_exporter-0.23.0.linux-amd64.tar.gz
--2023-01-09 21:26:39--  https://ghproxy.com/https://github.com/prometheus/blackbox_exporter/releases/download/v0.23.0/blackbox_exporter-0.23.0.linux-amd64.tar.gz
Resolving ghproxy.com (ghproxy.com)... 141.147.152.25
Connecting to ghproxy.com (ghproxy.com)|141.147.152.25|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 10831812 (10M) [application/octet-stream]
Saving to: ‘blackbox_exporter-0.23.0.linux-amd64.tar.gz’

100%[===========================================================================================================================================>] 10,831,812  2.25MB/s   in 5.2s   

2023-01-09 21:26:46 (1.97 MB/s) - ‘blackbox_exporter-0.23.0.linux-amd64.tar.gz’ saved [10831812/10831812]

```
# 安装
```yaml
# 解压
[root@VM-24-9-centos exporter_package]# tar -zxvf blackbox_exporter-0.23.0.linux-amd64.tar.gz 
blackbox_exporter-0.23.0.linux-amd64/
blackbox_exporter-0.23.0.linux-amd64/blackbox.yml
blackbox_exporter-0.23.0.linux-amd64/LICENSE
blackbox_exporter-0.23.0.linux-amd64/NOTICE
blackbox_exporter-0.23.0.linux-amd64/blackbox_exporter

# 备份配置文件
[root@VM-24-9-centos exporter_package]# cd blackbox_exporter-0.23.0.linux-amd64/
[root@VM-24-9-centos blackbox_exporter-0.23.0.linux-amd64]# ls
blackbox_exporter  blackbox.yml  LICENSE  NOTICE
[root@VM-24-9-centos blackbox_exporter-0.23.0.linux-amd64]# cp blackbox.yml blackbox.yml_init
[root@VM-24-9-centos blackbox_exporter-0.23.0.linux-amd64]# ls
blackbox_exporter  blackbox.yml  blackbox.yml_init  LICENSE  NOTICE
```
# blackbox_exporter配置文件demo
```yaml
scrape_configs:
  - job_name: 'blackbox'
    metrics_path: /probe
    params:
      module: [http_2xx]  # 加载一个模块为http_2xx的模块，这个模块用于查看http状态为200的响应
    static_configs:
      - targets:
        - http://prometheus.io    # 目标地址为http协议
        - https://prometheus.io   # 目标地址为https协议
        - http://example.com:8080 # 目标地址为http协议且端口为8080
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 127.0.0.1:9115  # The blackbox exporter's real hostname:port.
```
# 修改black_exporter配置文件
```yaml
[root@VM-24-9-centos blackbox_exporter-0.23.0.linux-amd64]# vi blackbox.yml
modules:
  http_2xx:# 这个名字需要和Prometheus中的params对应
    prober: http # 探针类型：http tcp  dns  icmp
    timeout: 10s
```
# 新增Prometheus配置文件job_name
```yaml
  - job_name: "blackbox_exporter"
    metrics_path: /probe # 默认为/probe
    params:
      module: [http_2xx] # 加载一个模块为http_2xx的模块，这个模块用于查看http状态为200的响应
    static_configs:
      - targets: # 要监控的目标地址
        - http://www.baidu.com/
        - http://prometheus.io
    relabel_configs: # 以下内容不要修改
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__address__]
        target_label: instance
      - target_label: __address__
        replacement: localhost:9115 # 该地址为blackbox_exporter服务的ip及端口
```
# 启动
```yaml
[root@VM-24-9-centos exporter_package]# cd blackbox_exporter-0.23.0.linux-amd64/
[root@VM-24-9-centos blackbox_exporter-0.23.0.linux-amd64]# ./blackbox_exporter --config.file="blackbox.yml"
ts=2023-01-09T14:39:45.219Z caller=main.go:78 level=info msg="Starting blackbox_exporter" version="(version=0.23.0, branch=HEAD, revision=26fc98b9c6db21457653ed752f34d1b7fb5bba43)"
ts=2023-01-09T14:39:45.219Z caller=main.go:79 level=info build_context="(go=go1.19.3, user=root@f360719453e3, date=20221202-12:26:32)"
ts=2023-01-09T14:39:45.220Z caller=main.go:91 level=info msg="Loaded config file"
ts=2023-01-09T14:39:45.220Z caller=tls_config.go:232 level=info msg="Listening on" address=[::]:9115
ts=2023-01-09T14:39:45.220Z caller=tls_config.go:235 level=info msg="TLS is disabled." http2=false address=[::]:9115

# 把blackbox_exporter服务挂到后台
nohup ./blackbox_exporter --config.file="blackbox.yml" &
```
# 显示效果
> 这里正好对应上面新增的两个监控目标

![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/prometheus_blackbox_1.png)

> 具体请求的结果可以访问 http://ip:9155访问
