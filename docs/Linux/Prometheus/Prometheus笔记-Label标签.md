# Label

Lable是为了方便管理及查询监控目标，在后续写promtheus查询语法的时候需要使用标签作为查询条件

# 配置文件

```yaml
# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # 定义一个job名称
  - job_name: "prometheus"

    # 默认指标地址 '/metrics'
  	metrics_path: '/metrics'
    # scheme defaults to 'http'.
    scheme: 'http'

	  # 静态指定每一个监控目标
    static_configs:
      # 监控目标节点地址，可以并列写入多个目标节点地址（格式为 机器ip：端口）,以逗号隔开
      - targets: ["localhost:9090"]
        # 标签
        labels:
          env: 'test'
```

上文配置文件17，18两行实现了新增一个label标签 `env`

# 显示效果

![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/prometheus_lable_1.png)
**注意：在修改配置文件后，需要重启Prometheus服务**