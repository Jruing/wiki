# 基于Grafana+Loki+Promatil搭建日志分析平台

## 简介

> 背景:
>
> 有很多厂商都用ELK(Elasticsearch+Logstash+Kibana)进行日志分析,ELK的用户体验确实很好,同时对于服务器的配置要求也不低,如果公司的项目规模不是很大,可以考虑考虑用GLP(Grafana+Loki+Promatil),GLP对服务器的要求没有ELK那么高,同时它部署起来也比ELK方便
>
> 
>
> ELK与Loki的优缺点(参考https://blog.csdn.net/gjjhyd/article/details/113624596):
>
> ![](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/ELK与loki优缺点.png)
>
> 
>
> 日志分析平台组成部分:
>
> Grafana: 用于日志的页面展示
>
> Loki: 服务端,负责存储收集到的日志,同时还负责处理日志的查询
>
> Promatil: 代理,负责收集日志并将收集到的日志发送到Loki

## 环境准备

> 腾讯云服务器: centos 7

## Grafana安装

>官方下载地址:https://dl.grafana.com/oss/release/grafana-8.4.0-1.x86_64.rpm
>
>:book:参考官方文档:https://grafana.com/docs/grafana/latest/installation/rpm/

### 安装步骤

#### 方案1(推荐):

新建配置(腾讯源) 参考:https://mirrors.cloud.tencent.com/help/grafana.html

```shell
vi /etc/yum.repos.d/grafana.repo
# 内容
[grafana]
name=grafana
baseurl=http://mirrors.cloud.tencent.com/grafana/yum/el7
repo_gpgcheck=0
gpgcheck=0
enabled=1
```

安装grafana

```shell
# 执行安装
sudo yum makecache
sudo yum install grafana

# 执行结果
[root@VM-24-9-centos src]# yum install grafana
Loaded plugins: fastestmirror, langpacks
Loading mirror speeds from cached hostfile
Resolving Dependencies
--> Running transaction check
---> Package grafana.x86_64 0:5.4.2-1 will be installed
--> Processing Dependency: urw-fonts for package: grafana-5.4.2-1.x86_64
--> Running transaction check
---> Package urw-base35-fonts.noarch 0:20170801-10.el7 will be installed
--> Processing Dependency: urw-base35-fonts-common = 20170801-10.el7 for package: urw-base35-fonts-20170801-10.el7.noarch
--> Processing Dependency: urw-base35-z003-fonts for package: urw-base35-fonts-20170801-10.el7.noarch
--> Processing Dependency: urw-base35-standard-symbols-ps-fonts for package: urw-base35-fonts-20170801-10.el7.noarch
--> Processing Dependency: urw-base35-p052-fonts for package: urw-base35-fonts-20170801-10.el7.noarch
--> Processing Dependency: urw-base35-nimbus-sans-fonts for package: urw-base35-fonts-20170801-10.el7.noarch
--> Processing Dependency: urw-base35-nimbus-roman-fonts for package: urw-base35-fonts-20170801-10.el7.noarch
--> Processing Dependency: urw-base35-nimbus-mono-ps-fonts for package: urw-base35-fonts-20170801-10.el7.noarch
--> Processing Dependency: urw-base35-gothic-fonts for package: urw-base35-fonts-20170801-10.el7.noarch
--> Processing Dependency: urw-base35-d050000l-fonts for package: urw-base35-fonts-20170801-10.el7.noarch
--> Processing Dependency: urw-base35-c059-fonts for package: urw-base35-fonts-20170801-10.el7.noarch
--> Processing Dependency: urw-base35-bookman-fonts for package: urw-base35-fonts-20170801-10.el7.noarch
--> Running transaction check
---> Package urw-base35-bookman-fonts.noarch 0:20170801-10.el7 will be installed
--> Processing Dependency: xorg-x11-server-utils for package: urw-base35-bookman-fonts-20170801-10.el7.noarch
--> Processing Dependency: xorg-x11-server-utils for package: urw-base35-bookman-fonts-20170801-10.el7.noarch
--> Processing Dependency: xorg-x11-font-utils for package: urw-base35-bookman-fonts-20170801-10.el7.noarch
--> Processing Dependency: xorg-x11-font-utils for package: urw-base35-bookman-fonts-20170801-10.el7.noarch
---> Package urw-base35-c059-fonts.noarch 0:20170801-10.el7 will be installed
---> Package urw-base35-d050000l-fonts.noarch 0:20170801-10.el7 will be installed
---> Package urw-base35-fonts-common.noarch 0:20170801-10.el7 will be installed
---> Package urw-base35-gothic-fonts.noarch 0:20170801-10.el7 will be installed
---> Package urw-base35-nimbus-mono-ps-fonts.noarch 0:20170801-10.el7 will be installed
---> Package urw-base35-nimbus-roman-fonts.noarch 0:20170801-10.el7 will be installed
---> Package urw-base35-nimbus-sans-fonts.noarch 0:20170801-10.el7 will be installed
---> Package urw-base35-p052-fonts.noarch 0:20170801-10.el7 will be installed
---> Package urw-base35-standard-symbols-ps-fonts.noarch 0:20170801-10.el7 will be installed
---> Package urw-base35-z003-fonts.noarch 0:20170801-10.el7 will be installed
--> Running transaction check
---> Package xorg-x11-font-utils.x86_64 1:7.5-21.el7 will be installed
--> Processing Dependency: libfontenc.so.1()(64bit) for package: 1:xorg-x11-font-utils-7.5-21.el7.x86_64
---> Package xorg-x11-server-utils.x86_64 0:7.7-20.el7 will be installed
--> Processing Dependency: libXxf86misc.so.1()(64bit) for package: xorg-x11-server-utils-7.7-20.el7.x86_64
--> Processing Dependency: libXt.so.6()(64bit) for package: xorg-x11-server-utils-7.7-20.el7.x86_64
--> Processing Dependency: libXmuu.so.1()(64bit) for package: xorg-x11-server-utils-7.7-20.el7.x86_64
--> Processing Dependency: libXmu.so.6()(64bit) for package: xorg-x11-server-utils-7.7-20.el7.x86_64
--> Processing Dependency: libICE.so.6()(64bit) for package: xorg-x11-server-utils-7.7-20.el7.x86_64
--> Running transaction check
---> Package libICE.x86_64 0:1.0.9-9.el7 will be installed
---> Package libXmu.x86_64 0:1.1.2-2.el7 will be installed
---> Package libXt.x86_64 0:1.1.5-3.el7 will be installed
--> Processing Dependency: libSM.so.6()(64bit) for package: libXt-1.1.5-3.el7.x86_64
---> Package libXxf86misc.x86_64 0:1.0.3-7.1.el7 will be installed
---> Package libfontenc.x86_64 0:1.1.3-3.el7 will be installed
--> Running transaction check
---> Package libSM.x86_64 0:1.2.2-2.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

====================================================================================================
 Package                                    Arch         Version                Repository     Size
====================================================================================================
Installing:
 grafana                                    x86_64       5.4.2-1                grafana        52 M
Installing for dependencies:
 libICE                                     x86_64       1.0.9-9.el7            os             66 k
 libSM                                      x86_64       1.2.2-2.el7            os             39 k
 libXmu                                     x86_64       1.1.2-2.el7            os             71 k
 libXt                                      x86_64       1.1.5-3.el7            os            173 k
 libXxf86misc                               x86_64       1.0.3-7.1.el7          os             19 k
 libfontenc                                 x86_64       1.1.3-3.el7            os             31 k
 urw-base35-bookman-fonts                   noarch       20170801-10.el7        os            852 k
 urw-base35-c059-fonts                      noarch       20170801-10.el7        os            879 k
 urw-base35-d050000l-fonts                  noarch       20170801-10.el7        os             75 k
 urw-base35-fonts                           noarch       20170801-10.el7        os            7.6 k
 urw-base35-fonts-common                    noarch       20170801-10.el7        os             19 k
 urw-base35-gothic-fonts                    noarch       20170801-10.el7        os            650 k
 urw-base35-nimbus-mono-ps-fonts            noarch       20170801-10.el7        os            796 k
 urw-base35-nimbus-roman-fonts              noarch       20170801-10.el7        os            860 k
 urw-base35-nimbus-sans-fonts               noarch       20170801-10.el7        os            1.3 M
 urw-base35-p052-fonts                      noarch       20170801-10.el7        os            978 k
 urw-base35-standard-symbols-ps-fonts       noarch       20170801-10.el7        os             40 k
 urw-base35-z003-fonts                      noarch       20170801-10.el7        os            275 k
 xorg-x11-font-utils                        x86_64       1:7.5-21.el7           os            104 k
 xorg-x11-server-utils                      x86_64       7.7-20.el7             os            178 k

Transaction Summary
====================================================================================================
Install  1 Package (+20 Dependent packages)

Total download size: 60 M
Installed size: 65 M
Is this ok [y/d/N]: y
Downloading packages:
(1/21): libICE-1.0.9-9.el7.x86_64.rpm                                        |  66 kB  00:00:00     
(2/21): libSM-1.2.2-2.el7.x86_64.rpm                                         |  39 kB  00:00:00     
(3/21): libXmu-1.1.2-2.el7.x86_64.rpm                                        |  71 kB  00:00:00     
(4/21): libXt-1.1.5-3.el7.x86_64.rpm                                         | 173 kB  00:00:00     
(5/21): libXxf86misc-1.0.3-7.1.el7.x86_64.rpm                                |  19 kB  00:00:00     
(6/21): libfontenc-1.1.3-3.el7.x86_64.rpm                                    |  31 kB  00:00:00     
(7/21): urw-base35-bookman-fonts-20170801-10.el7.noarch.rpm                  | 852 kB  00:00:00     
(8/21): urw-base35-d050000l-fonts-20170801-10.el7.noarch.rpm                 |  75 kB  00:00:00     
(9/21): urw-base35-fonts-20170801-10.el7.noarch.rpm                          | 7.6 kB  00:00:00     
(10/21): urw-base35-c059-fonts-20170801-10.el7.noarch.rpm                    | 879 kB  00:00:00     
(11/21): urw-base35-fonts-common-20170801-10.el7.noarch.rpm                  |  19 kB  00:00:00     
(12/21): urw-base35-nimbus-mono-ps-fonts-20170801-10.el7.noarch.rpm          | 796 kB  00:00:00     
(13/21): urw-base35-gothic-fonts-20170801-10.el7.noarch.rpm                  | 650 kB  00:00:00     
(14/21): urw-base35-nimbus-roman-fonts-20170801-10.el7.noarch.rpm            | 860 kB  00:00:00     
(15/21): urw-base35-p052-fonts-20170801-10.el7.noarch.rpm                    | 978 kB  00:00:00     
(16/21): urw-base35-standard-symbols-ps-fonts-20170801-10.el7.noarch.rpm     |  40 kB  00:00:00     
(17/21): urw-base35-nimbus-sans-fonts-20170801-10.el7.noarch.rpm             | 1.3 MB  00:00:00     
(18/21): urw-base35-z003-fonts-20170801-10.el7.noarch.rpm                    | 275 kB  00:00:00     
(19/21): xorg-x11-server-utils-7.7-20.el7.x86_64.rpm                         | 178 kB  00:00:00     
(20/21): xorg-x11-font-utils-7.5-21.el7.x86_64.rpm                           | 104 kB  00:00:00     
(21/21): grafana-5.4.2-1.x86_64.rpm                                          |  52 MB  00:00:43     
----------------------------------------------------------------------------------------------------
Total                                                               1.4 MB/s |  60 MB  00:00:43     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : urw-base35-fonts-common-20170801-10.el7.noarch                                  1/21 
  Installing : libICE-1.0.9-9.el7.x86_64                                                       2/21 
  Installing : libSM-1.2.2-2.el7.x86_64                                                        3/21 
  Installing : libXt-1.1.5-3.el7.x86_64                                                        4/21 
  Installing : libXmu-1.1.2-2.el7.x86_64                                                       5/21 
  Installing : libfontenc-1.1.3-3.el7.x86_64                                                   6/21 
  Installing : 1:xorg-x11-font-utils-7.5-21.el7.x86_64                                         7/21 
  Installing : libXxf86misc-1.0.3-7.1.el7.x86_64                                               8/21 
  Installing : xorg-x11-server-utils-7.7-20.el7.x86_64                                         9/21 
  Installing : urw-base35-c059-fonts-20170801-10.el7.noarch                                   10/21 
  Installing : urw-base35-z003-fonts-20170801-10.el7.noarch                                   11/21 
  Installing : urw-base35-nimbus-mono-ps-fonts-20170801-10.el7.noarch                         12/21 
  Installing : urw-base35-d050000l-fonts-20170801-10.el7.noarch                               13/21 
  Installing : urw-base35-p052-fonts-20170801-10.el7.noarch                                   14/21 
  Installing : urw-base35-nimbus-roman-fonts-20170801-10.el7.noarch                           15/21 
  Installing : urw-base35-standard-symbols-ps-fonts-20170801-10.el7.noarch                    16/21 
  Installing : urw-base35-bookman-fonts-20170801-10.el7.noarch                                17/21 
  Installing : urw-base35-nimbus-sans-fonts-20170801-10.el7.noarch                            18/21 
  Installing : urw-base35-gothic-fonts-20170801-10.el7.noarch                                 19/21 
  Installing : urw-base35-fonts-20170801-10.el7.noarch                                        20/21 
  Installing : grafana-5.4.2-1.x86_64                                                         21/21 
### NOT starting on installation, please execute the following statements to configure grafana to start automatically using systemd
 sudo /bin/systemctl daemon-reload
 sudo /bin/systemctl enable grafana-server.service
### You can start grafana-server by executing
 sudo /bin/systemctl start grafana-server.service
POSTTRANS: Running script
  Verifying  : urw-base35-fonts-20170801-10.el7.noarch                                         1/21 
  Verifying  : grafana-5.4.2-1.x86_64                                                          2/21 
  Verifying  : libXmu-1.1.2-2.el7.x86_64                                                       3/21 
  Verifying  : urw-base35-c059-fonts-20170801-10.el7.noarch                                    4/21 
  Verifying  : libSM-1.2.2-2.el7.x86_64                                                        5/21 
  Verifying  : urw-base35-z003-fonts-20170801-10.el7.noarch                                    6/21 
  Verifying  : urw-base35-nimbus-mono-ps-fonts-20170801-10.el7.noarch                          7/21 
  Verifying  : urw-base35-d050000l-fonts-20170801-10.el7.noarch                                8/21 
  Verifying  : libXt-1.1.5-3.el7.x86_64                                                        9/21 
  Verifying  : urw-base35-p052-fonts-20170801-10.el7.noarch                                   10/21 
  Verifying  : urw-base35-nimbus-roman-fonts-20170801-10.el7.noarch                           11/21 
  Verifying  : 1:xorg-x11-font-utils-7.5-21.el7.x86_64                                        12/21 
  Verifying  : urw-base35-standard-symbols-ps-fonts-20170801-10.el7.noarch                    13/21 
  Verifying  : urw-base35-bookman-fonts-20170801-10.el7.noarch                                14/21 
  Verifying  : libICE-1.0.9-9.el7.x86_64                                                      15/21 
  Verifying  : libXxf86misc-1.0.3-7.1.el7.x86_64                                              16/21 
  Verifying  : libfontenc-1.1.3-3.el7.x86_64                                                  17/21 
  Verifying  : xorg-x11-server-utils-7.7-20.el7.x86_64                                        18/21 
  Verifying  : urw-base35-fonts-common-20170801-10.el7.noarch                                 19/21 
  Verifying  : urw-base35-nimbus-sans-fonts-20170801-10.el7.noarch                            20/21 
  Verifying  : urw-base35-gothic-fonts-20170801-10.el7.noarch                                 21/21 

Installed:
  grafana.x86_64 0:5.4.2-1                                                                          

Dependency Installed:
  libICE.x86_64 0:1.0.9-9.el7                                                                       
  libSM.x86_64 0:1.2.2-2.el7                                                                        
  libXmu.x86_64 0:1.1.2-2.el7                                                                       
  libXt.x86_64 0:1.1.5-3.el7                                                                        
  libXxf86misc.x86_64 0:1.0.3-7.1.el7                                                               
  libfontenc.x86_64 0:1.1.3-3.el7                                                                   
  urw-base35-bookman-fonts.noarch 0:20170801-10.el7                                                 
  urw-base35-c059-fonts.noarch 0:20170801-10.el7                                                    
  urw-base35-d050000l-fonts.noarch 0:20170801-10.el7                                                
  urw-base35-fonts.noarch 0:20170801-10.el7                                                         
  urw-base35-fonts-common.noarch 0:20170801-10.el7                                                  
  urw-base35-gothic-fonts.noarch 0:20170801-10.el7                                                  
  urw-base35-nimbus-mono-ps-fonts.noarch 0:20170801-10.el7                                          
  urw-base35-nimbus-roman-fonts.noarch 0:20170801-10.el7                                            
  urw-base35-nimbus-sans-fonts.noarch 0:20170801-10.el7                                             
  urw-base35-p052-fonts.noarch 0:20170801-10.el7                                                    
  urw-base35-standard-symbols-ps-fonts.noarch 0:20170801-10.el7                                     
  urw-base35-z003-fonts.noarch 0:20170801-10.el7                                                    
  xorg-x11-font-utils.x86_64 1:7.5-21.el7                                                           
  xorg-x11-server-utils.x86_64 0:7.7-20.el7                                                         

Complete!
```

#### 方案2:

```shell
# 下载grafana 包
wget https://dl.grafana.com/oss/release/grafana-8.4.0-1.x86_64.rpm
# 安装grafana
sudo yum install grafana-8.4.0-1.x86_64.rpm
```

#### 启动服务:

```shell
# 重载grafana服务的配置文件
sudo systemctl daemon-reload

# 启动grafana服务
sudo systemctl start grafana-server


# 查看grafana服务状态
sudo systemctl status grafana-server
[root@VM-24-9-centos ~]$ systemctl status grafana-server
● grafana-server.service - Grafana instance
   Loaded: loaded (/usr/lib/systemd/system/grafana-server.service; disabled; vendor preset: disabled)
   Active: active (running) since Wed 2022-03-30 14:01:58 CST; 4min 42s ago
     Docs: http://docs.grafana.org
 Main PID: 6213 (grafana-server)
    Tasks: 13
   Memory: 13.1M
   CGroup: /system.slice/grafana-server.service
           └─6213 /usr/sbin/grafana-server --config=/etc/grafana/grafana.ini --pidfile=/var/run/g...

# 停止grafana服务
sudo systemctl stop grafana-server
```

#### 配置Grafana

略

## Loki安装

> 下载地址:https://github.com/grafana/loki/releases/download/v2.4.2/loki-linux-amd64.zip
>
> Loki默认配置文件下载地址:https://raw.githubusercontent.com/grafana/loki/master/cmd/loki/loki-local-config.yaml
>
> :book:参考官方文档:https://grafana.com/docs/loki/latest/installation/local/

### 安装步骤

#### 下载Loki

```shell
# 由于服务器访问github有点慢,所以采用了代理加速
wget https://shrill-pond-3e81.hunsh.workers.dev/https://github.com/grafana/loki/releases/download/v2.4.2/loki-linux-amd64.zip

# 解压
unzip loki-linux-amd64.zip 
```

#### 下载配置文件

```shell
wget https://shrill-pond-3e81.hunsh.workers.dev/https://raw.githubusercontent.com/grafana/loki/master/cmd/loki/loki-local-config.yaml
```

### Loki配置文件调整

```yaml
auth_enabled: false
 
server:
  http_listen_port: 3100 # 监听端口
 
ingester:
  lifecycler:
    address: 0.0.0.0 # 监听地址
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
    final_sleep: 0s
  chunk_idle_period: 5m
  chunk_retain_period: 30s
  max_transfer_retries: 0
 
schema_config:
  configs:
    - from: 2018-04-15
      store: boltdb
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 144h  #  每张表的时间范围 6天
      chunks:
        period: 144h
 
storage_config:
#  流文件存储地址
  boltdb:
    directory: /tmp/loki/index
#  索引存储地址
  filesystem:
    directory: /tmp/loki/chunks
 
limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 144h
 
chunk_store_config:
  max_look_back_period: 2160h  # 最大可查询历史日期 90天
 

table_manager:   # 表的保留期90天
  retention_deletes_enabled: true
  retention_period: 720h
```

## Promtail安装

> 下载地址:https://github.com/grafana/loki/releases/download/v2.4.2/promtail-linux-amd64.zip
>
> Promtail默认配置文件下载地址:https://raw.githubusercontent.com/grafana/loki/main/clients/cmd/promtail/promtail-local-config.yaml
>
> :book:参考官方文档:https://grafana.com/docs/loki/latest/installation/local/

### 安装步骤

#### 下载Promtail

```shell
# 由于服务器访问github有点慢,所以采用了代理加速
wget https://shrill-pond-3e81.hunsh.workers.dev/https://github.com/grafana/loki/releases/download/v2.4.2/promtail-linux-amd64.zip

# 解压
unzip promtail-linux-amd64.zip
```

#### 下载配置文件

```shell
wget https://shrill-pond-3e81.hunsh.workers.dev/https://raw.githubusercontent.com/grafana/loki/main/clients/cmd/promtail/promtail-local-config.yaml
```

### Promtail配置文件

```
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://localhost:3100/loki/api/v1/push

scrape_configs:
- job_name: logs
  pipeline_stages:
  - match:
      selector: '{job="日志分析平台"}'
      stages:
        - regex:
            expression: ^(?P<timestamp>\d+-\d+-\d+.\d+:\d+:\d+) - (?P<threadid>\d{3,6}) - (?P<level>INFO|ERROR|WARNING) - (?P<filename>.*?) - (?P<lineno>\d+) - (?P<requestid>\d+) - (?P<systemname>.*?) - (?P<message>.*?)$
        - labels:
            timestamp:
            threadid:
            level:
            filename:
            lineno:
            requestid:
            systemname:
            message:
  static_configs:
  - targets:
      - localhost
    labels:
      job: 日志分析平台 # labels名称
      __path__: C://Users//Jruing//Desktop//Automation_Testing//yunwei_info.log # 采集日志的路径

```
