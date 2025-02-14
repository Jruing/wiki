> 一般一个job作为一个业务服务，它下面的监控的机器/节点都是这个服务的节点，为了方便管理，我们可以按照job划分，为每个job创建一个子配置文件，这样方便管理

# 配置文件

```yaml
# my global config
global:
  scrape_interval: 15s # #每15s采集一次数据
  evaluation_interval: 15s #每15s做一次告警检测.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration(告警配置)
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

# rule_files 加载告警规则文件
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # 定义一个job名称
  - job_name: "prometheus"

    # 默认指标地址 '/metrics'
  	metrics_path: '/metrics'
    # scheme defaults to 'http'.
    scheme: 'http'

	  # 基于文件的服务发现提供了一种更通用的方法来配置静态目标，子配置文件支持json和yaml
    file_sd_configs:
      - files: ["./child_config/prometheus.yml"]
```

# 创建子配置文件目录

```shell
[root@VM-24-9-centos prometheus-2.41.0.linux-amd64]# mkdir -p child_config
```

# 创建子配置文件

```shell
[root@VM-24-9-centos prometheus-2.41.0.linux-amd64]# cd child_config
[root@VM-24-9-centos prometheus-2.41.0.linux-amd64]# touch prometheus.yml
```

```yaml
- targets: ["localhost:9090"]
  labels:
    env: 'test'
    host: 'localhost'
```

# 显示效果

![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/prometheus_file_sd_1.png)