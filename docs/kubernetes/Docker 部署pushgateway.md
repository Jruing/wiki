## 拉取镜像
```
[root@VM-24-9-centos ~]# docker pull prom/pushgateway
Using default tag: latest
latest: Pulling from prom/pushgateway
22b70bddd3ac: Pull complete 
5c12815fee55: Pull complete 
c82d45e6b5e4: Pull complete 
669d401920b2: Pull complete 
Digest: sha256:28fe26c8b8b183ad6f6208936d678d875097b0635ffdffc41dfa734afd71ed17
Status: Downloaded newer image for prom/pushgateway:latest
docker.io/prom/pushgateway:latest
```
## 启动pushgateway
```
docker run -itd --name=pushgateway \
-p 9091:9091 \
--network prom-network \
prom/pushgateway
# --network 这个参数可以不写，为了配合上一篇文章中Prometheus网络
```

## 手动推送数据
```
# 默认 URL 地址为：http://<ip>:9091/metrics/job/<JOBNAME>{/<LABEL_NAME>/<LABEL_VALUE>}，
# 是必填项，为 job 标签值，后边可以跟任意数量的标签对，一般我们会添加一个 instance/<INSTANCE_NAME>实例名称标签，来方便区分各个指标。

echo "request_error_number 99" | curl --data-binary @- http://172.18.0.3:9091/metrics/job/link_job
```

## 页面预览
地址为：http://ip:9091
![image](https://img2023.cnblogs.com/blog/1889313/202302/1889313-20230216223636879-423627240.png)

