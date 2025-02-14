# Grafana官网
# 下载Grafana
```yaml
[root@VM-24-9-centos Prometheus_server]# wget httpsdl.grafana.comossreleasegrafana-9.3.2.linux-amd64.tar.gz
```
# 安装Grafana
```yaml
[root@VM-24-9-centos Prometheus_server]# tar -zxvf grafana-9.3.2.linux-amd64.tar.gz
[root@VM-24-9-centos Prometheus_server]# cd grafana-9.3.2bin
# 启动Grafana
[root@VM-24-9-centos bin]# nohup .grafana-server &
```
# 配置Grafana
 端口默认3000，访问地址 localhost3000，默认账号密码 adminadmin

## 选择数据源
![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/prometheus_grafana_1.png)
![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/prometheus_grafana_2.png)
![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/prometheus_grafana_3.png)
![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/prometheus_grafana_4.png)

## 选择dashboard
 我们可以根据数据源查询合适的dashboard仪表盘，这里我们选择第一个，如果没有自己喜欢的，可以自己在grafana里编写，小白还是直接用现成的轮子吧，嘻嘻

![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/prometheus_grafana_5.png)
![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/prometheus_grafana_6.png)
![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/prometheus_grafana_7.png)
![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/prometheus_grafana_8.png)
![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/prometheus_grafana_9.png)

# 显示效果
 dashboard包含了CPU，内存，网络，磁盘，io等信息

![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/prometheus_grafana_10.png)
![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/prometheus_grafana_11.png)
