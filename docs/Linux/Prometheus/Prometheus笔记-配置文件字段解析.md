# 全局配置注解

```shell
global:
  # 默认情况抓取目标的频率，默认1分钟
  [ scrape_interval: <duration> | default = 1m ]
  # 抓取请求超时的时间，默认10S
  [ scrape_timeout: <duration> | default = 10s ]
  # 评估规则的频率，默认1分钟
  [ evaluation_interval: <duration> | default = 1m ]
  # 在与进行通信时要添加到任何时间序列或警报的标签
  # 外部系统（federation、远程、storage、Alertmanager）
  external_labels:
    [ <labelname>: <labelvalue> ... ]
  # PromQL查询记录到的文件。重新加载配置将重新打开该文件。
  [ query_log_file: <string> ]
# 规则文件指定全局的列表。从中读取规则和警报。
rule_files:
  [ - <filepath_glob> ... ]
# 抓取配置的列表
scrape_configs:
  [ - <scrape_config> ... ]
# 警报指定与Alertmanager相关的设置
alerting:
  alert_relabel_configs:
    [ - <relabel_config> ... ]
  alertmanagers:
    [ - <alertmanager_config> ... ]

# 与远程写入功能相关的设置
remote_write:
  [ - <remote_write> ... ]
# 与远程读取功能相关的设置。
remote_read:
  [ - <remote_read> ... ]

```

# Scrape_config配置注解

```shell
# 默认情况下，分配给临时度量的作业名称。
job_name: <job_name>
# 从这项工作中抓取目标的频率。
[ scrape_interval: <duration> | default = <global_config.scrape_interval> ]
# 此作业时的每次抓取超时时间
[ scrape_timeout: <duration> | default = <global_config.scrape_timeout> ]
# 要从目标获取度量的HTTP资源路径
[ metrics_path: <path> | default = /metrics ]
# honor_labels主要用于解决prometheus server的label与exporter端用户自定义label冲突的问题。
# 为“true”，则通过保留标签来解决标签冲突值，并忽略冲突的服务器端标签。
# 为“false”，则通过重命名解决标签冲突
[ honor_labels: <boolean> | default = false ]
# 如果honor_timestamps设置为“true”，则将显示度量的时间戳由目标将被使用。
# 为“false”，则会显示度量的时间戳，将忽略由目标创建的。
[ honor_timestamps: <boolean> | default = true ]
# 配置用于请求的协议方案。
[ scheme: <scheme> | default = http ]
# 可选的HTTP URL参数
params:
  [ <string>: [<string>, ...] ]
# 使用配置的用户名和密码，密码和密码文件是互斥的。
basic_auth:
  [ username: <string> ]
  [ password: <secret> ]
  [ password_file: <string> ]
# 使用设置每个刮取请求的“Authorization”标头为配置的凭据。
authorization:
  # 设置请求的请求头身份验证类型。
  [ type: <string> | default: Bearer ]
  # 设置请求的凭据。这是和credentials_file相互排斥的
  [ credentials: <secret> ]
  # 使用从中读取的凭据设置请求的凭据
  [ credentials_file: <filename> ]
# 可选的OAuth 2.0配置。不能与基本授权或授权同时使用。
oauth2:
  [ <oauth2> ]
# 配置抓取请求是否遵循HTTP 3xx重定向。
[ follow_redirects: <bool> | default = true ]
# 配置请求的TLS设置。
tls_config:
  [ <tls_config> ]
# 可选的代理URL
[ proxy_url: <string> ]
# 
azure_sd_configs:
  [ - <azure_sd_config> ... ]
# consul服务发现配置的列表。
consul_sd_configs:
  [ - <consul_sd_config> ... ]
# digitalocean服务发现配置的列表。
digitalocean_sd_configs:
  [ - <digitalocean_sd_config> ... ]
# docker服务发现配置的列表。
docker_sd_configs:
  [ - <docker_sd_config> ... ]
# dockerswarm服务发现配置的列表。
dockerswarm_sd_configs:
  [ - <dockerswarm_sd_config> ... ]
# dns 服务发现配置的列表。
dns_sd_configs:
  [ - <dns_sd_config> ... ]
# ec2 服务发现配置的列表。
ec2_sd_configs:
  [ - <ec2_sd_config> ... ]
# eureka 服务发现配置的列表。
eureka_sd_configs:
  [ - <eureka_sd_config> ... ]
# eureka 服务发现配置的列表。
file_sd_configs:
  [ - <file_sd_config> ... ]

# eureka 服务发现配置的列表。
gce_sd_configs:
  [ - <gce_sd_config> ... ]

# List of Hetzner service discovery configurations.
hetzner_sd_configs:
  [ - <hetzner_sd_config> ... ]

# List of HTTP service discovery configurations.
http_sd_configs:
  [ - <http_sd_config> ... ]

# List of Kubernetes service discovery configurations.
kubernetes_sd_configs:
  [ - <kubernetes_sd_config> ... ]

# List of Kuma service discovery configurations.
kuma_sd_configs:
  [ - <kuma_sd_config> ... ]
# 省略其他服务发现。。。。
# 此作业的标记静态配置目标列表。
static_configs:
  [ - <static_config> ... ]
# 目标重新标记配置的列表。
relabel_configs:
  [ - <relabel_config> ... ]
# 公制重新标记配置的列表。
metric_relabel_configs:
  [ - <relabel_config> ... ]
# 如果未压缩的响应正文大于这么多字节，则会导致,勉强失败。0表示没有限制。例如：100MB。
# 这是一个实验特性，这种行为可能在将来更改或删除。
[ body_size_limit: <size> | default = 0 ]
# 每个抓取限制将被接受的刮取样品数量。
#如果在公制重新标记后存在超过此数量的样本
#整个抓取将被视为失败。0表示没有限制。
[ sample_limit: <int> | default = 0 ]
# 每抓取一次可接受的标签数量限制。如果超过这个数量的标签在度量重新标记后出现。整个将被视为失败。0表示没有限制。
[ label_limit: <int> | default = 0 ]
# 样本可接受的标签名称长度的每抓取限制。如果标签名称长于此数字，则在重新标记度量后，整个将被视为失败。0表示没有限制。
[ label_name_length_limit: <int> | default = 0 ]
# 标签长度的每次抓取限制值，该值将被样本接受。
[ label_value_length_limit: <int> | default = 0 ]
# 每个抓取配置对将被删除的唯一目标数的限制接受。如果目标后存在的目标数量超过此数量
#重新标记后，普罗米修斯将在不清除目标的情况下将目标标记为失败。0表示没有限制。
[ target_limit: <int> | default = 0 

```

# 告警配置注解

```shell
# 推送警报时每个目标Alertmanager超时时间
[ timeout: <duration> | default = 10s ]
# Alertmanager的api版本
[ api_version: <string> | default = v2 ]
# 被推送HTTP路径警报的前缀
[ path_prefix: <path> | default = / ]
# 配置用于请求的协议方案。
[ scheme: <scheme> | default = http ]
# 配置认证信息
basic_auth:
  [ username: <string> ]
  [ password: <secret> ]
  [ password_file: <string> ]
authorization:
  [ type: <string> | default: Bearer ]
  [ credentials: <secret> ]
  [ credentials_file: <filename> ]
oauth2:
  [ <oauth2> ]
tls_config:
  [ <tls_config> ]
[ proxy_url: <string> ]
[ follow_redirects: <bool> | default = true ]
# List of Azure service discovery configurations.
azure_sd_configs:
  [ - <azure_sd_config> ... ]
# 省略其他服务发现配置
# Alertmanagers的static_config集合
static_configs:
  [ - <static_config> ... ]
# Alertmanager  的relabel_configs配置集合
relabel_configs:
  [ - <relabel_config> ... ]
```

# 静态配置注解

```shell
# 目标的主机地址
targets:
  [ - '<host>' ]
# 分配给从目标中抓取的所有度量的标签
labels:
  [ <labelname>: <labelvalue> ... ]
```