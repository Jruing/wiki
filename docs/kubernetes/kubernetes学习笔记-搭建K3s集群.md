# kubernetes学习笔记

## 基础环境

> 系统镜像版本
>
> * Centos 7.6 最小化
>
> 最低运行环境基本要求
>
> * 内存及CPU：512MB / CPU 1核
>
> K3s版本
>
> * v1.30.0+k3s1
>
> 集群规划:
>
> `注意`：需要对每台主机设置`hostname`,使用` hostnamectl set-hostname 主机名`
>
> * K8s-master   192.168.200.129 1C/1G
> * K8s-worker1 192.168.200.130 2C/2G
> * K8s-worker2 192.168.200.131 2C/2G

## 准备工作

1. 关闭防火墙

   `systemctl disable firewalld --now`

2. 设置Selinux(需要接入互联网)

   `yum install -y container-selinux selinux-policy-base
   yum install -y https://rpm.rancher.io/k3s/latest/common/centos/7/noarch/k3s-selinux-0.2-1.el7_8.noarch.rpm`

3. 免密登录

   ```
   ssh-keygen -t rsa
   ssh-copy-id -i /root/.ssh/id_rsa.pub 192.168.200.130
   ssh-copy-id -i /root/.ssh/id_rsa.pub 192.168.200.131
   ```


## 安装K3s集群

> K3s集群分为`K3s server`（控制平面） 及 `k3s agent` （工作节点）

* 在`k8s-master` 节点安装`k3s server`

    ```shell
    curl -sfL https://rancher-mirror.rancher.cn/k3s/k3s-install.sh | INSTALL_K3S_MIRROR=cn sh -
    ```

## 卸载K3s集群

```
k3s-uninstall.sh
```

## 验证安装

* 查看节点状态 `kubectl get node`

    ```
    [root@localhost ~]# kubectl get node
    NAME         STATUS   ROLES                  AGE   VERSION
    k8s-master   Ready    control-plane,master   16s   v1.30.4+k3s1
    ```

* 查看token `cat /var/lib/rancher/k3s/server/node-token`

  > 这个token用于`K8s-worker1`和`K8s-worker2`这两个节点加入集群

    ```
    [root@localhost ~]# cat /var/lib/rancher/k3s/server/node-token
    K103b59c9e5e4a8904ad2f4ba0dc2fc17079af59e8cd3f8f7c51f5a42d62a373eb0::server:e2b46796a195fe2a86de36c54855802e
    ```

## 节点加入集群

> 分别在`k8s-worker1` 和 `k8s-worker2` 两台主机分别执行以下命令

```
curl -sfL https://rancher-mirror.rancher.cn/k3s/k3s-install.sh | INSTALL_K3S_MIRROR=cn K3S_URL=https://192.168.200.129:6443 K3S_TOKEN=K103b59c9e5e4a8904ad2f4ba0dc2fc17079af59e8cd3f8f7c51f5a42d62a373eb0::server:e2b46796a195fe2a86de36c54855802e sh -
```

> 在`k8s-master`节点执行`kubectl get node`，可以看到`k8s-worker1` 和 `k8s-worker2` 已经加入集群

```
[root@k8s-master ~]# kubectl get node
NAME          STATUS   ROLES                  AGE     VERSION
k8s-master    Ready    control-plane,master   57m     v1.30.4+k3s1
k8s-worker1   Ready    <none>                 4m46s   v1.30.4+k3s1
k8s-worker2   Ready    <none>                 3m33s   v1.30.4+k3s1
```

## 镜像加速

1. `k8s-master`节点添加镜像加速配置文件 `/etc/rancher/k3s/registries.yaml`

    ```
    mirrors:
      docker.io:
        endpoint:
          - "https://hub.uuuadc.top"
          - "https://docker.anyhub.us.kg"
          - "https://dockerhub.jobcher.com"
          - "https://dockerhub.icu"
          - "https://docker.ckyl.me"
          - "https://docker.awsl9527.cn"
    ```

2. 分发到`k8s-worker1` 和 `k8s-worker2` 

    ```
    scp /etc/rancher/k3s/registries.yaml root@192.168.200.130:/etc/rancher/k3s/registries.yaml
    scp /etc/rancher/k3s/registries.yaml root@192.168.200.131:/etc/rancher/k3s/registries.yaml
    ```

3. 重启`k3s-server`及`k3s-agent`

    ```
    # 在k8s-master节点执行
    systemctl restart k3s
    # 在k8s-worker1和k8s-worker2节点执行
    systemctl restart k3s-agent
    ```

4. 验证

    ```
    # 拉取mysql镜像
    [root@k8s-master ~]# crictl pull mysql:5.7-debian
    Image is up to date for sha256:6dca1336186922918678a49811059c4f6bfa1759d853a4e7cde904879d2e9b83
    # 查看镜像列表
    [root@k8s-master ~]# crictl  images
    IMAGE                     TAG                 IMAGE ID            SIZE
    docker.io/library/mysql   5.7-debian          6dca133618692       163MB
    ```

  ## Pod

* 创建Pod资源 `kubectl run`

  ```
  # 创建一个名称为 mynginx，镜像为 nginx 的Pod
  [root@k8s-master ~]# kubectl run mynginx --image=nginx
  pod/mynginx created
  ```
  
* 查看Pod `kubectl get pod`

  ```
  [root@k8s-master ~]# kubectl get pod
  NAME      READY   STATUS    RESTARTS   AGE
  mynginx   1/1     Running   0          11m
  # 显示pod的IP和运行节点信息
  [root@k8s-master ~]# kubectl get pod -owide
  NAME      READY   STATUS    RESTARTS   AGE     IP          NODE          NOMINATED NODE   READINESS GATES
  mynginx   1/1     Running   0          4m40s   10.42.2.3   k8s-worker2   <none>           <none>
  ```

* 查看Pod运行日志 `kubectl logs`

    ```
    [root@k8s-master ~]# kubectl logs mynginx
    /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
    /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
    /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
    10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
    10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
    /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
    /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
    /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
    /docker-entrypoint.sh: Configuration complete; ready for start up
    2024/08/24 05:50:48 [notice] 1#1: using the "epoll" event method
    2024/08/24 05:50:48 [notice] 1#1: nginx/1.27.1
    2024/08/24 05:50:48 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14) 
    2024/08/24 05:50:48 [notice] 1#1: OS: Linux 3.10.0-1160.el7.x86_64
    2024/08/24 05:50:48 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
    2024/08/24 05:50:48 [notice] 1#1: start worker processes
    2024/08/24 05:50:48 [notice] 1#1: start worker process 29
    2024/08/24 05:50:48 [notice] 1#1: start worker process 30
    2024/08/24 05:50:48 [notice] 1#1: start worker process 31
    2024/08/24 05:50:48 [notice] 1#1: start worker process 32
    10.42.0.0 - - [24/Aug/2024:05:51:59 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/7.29.0" "-"
    ```

* 查看Pod详细信息

  ```
  [root@k8s-master ~]# kubectl describe pod mynginx
  Name:             mynginx
  Namespace:        default
  Priority:         0
  Service Account:  default
  Node:             k8s-worker2/192.168.200.131
  Start Time:       Sat, 24 Aug 2024 13:46:18 +0800
  Labels:           run=mynginx
  Annotations:      <none>
  Status:           Pending
  IP:               
  IPs:              <none>
  Containers:
    mynginx:
      Container ID:   
      Image:          nginx
      Image ID:       
      Port:           <none>
      Host Port:      <none>
      State:          Waiting
        Reason:       ContainerCreating
      Ready:          False
      Restart Count:  0
      Environment:    <none>
      Mounts:
        /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-w4xqw (ro)
  Conditions:
    Type                        Status
    PodReadyToStartContainers   False 
    Initialized                 True 
    Ready                       False 
    ContainersReady             False 
    PodScheduled                True 
  Volumes:
    kube-api-access-w4xqw:
      Type:                    Projected (a volume that contains injected data from multiple sources)
      TokenExpirationSeconds:  3607
      ConfigMapName:           kube-root-ca.crt
      ConfigMapOptional:       <nil>
      DownwardAPI:             true
  QoS Class:                   BestEffort
  Node-Selectors:              <none>
  Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                               node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
  Events:
    Type    Reason     Age   From               Message
    ----    ------     ----  ----               -------
    Normal  Scheduled  13s   default-scheduler  Successfully assigned default/mynginx to k8s-worker2
  ```

  

* 在容器中执行命令 `kubectl exec`

  ```
  kubectl exec mynginx -it -- /bin/bash
  ```

* 删除Pod `kubectl delete`

  ```
  # 删除Pod
  kubectl delete pod mynginx
  # 强制删除
  kubectl delete pod mynginx --force
  ```


## Deployment与ReplicaSet

> * Deployment使Pod具有自愈的能力，当我们删除Deployment中的一个或多个pod后，他会自动创建Pod直到与副本数量一致
> * Deployment使Pod具有滚动更新及版本回退的能力

* 创建Deployment `kubectl create deployment`
  ```
  # 创建一个deployment资源，名称为nginx-deployment，镜像为nginx:1.22 ，副本数量为3
  [root@k8s-master ~]# kubectl create deployment nginx-deployment --image=nginx:1.22 --replicas=3
  deployment.apps/nginx-deployment created
  ```

* 查看Deployment

  ```
  [root@k8s-master ~]# kubectl get deploy 
  NAME               READY   UP-TO-DATE   AVAILABLE   AGE
  nginx-deployment   3/3     3            3           5m9s
  ```

* 查看Pod

  ```
  [root@k8s-master ~]# kubectl get pod
  NAME                                READY   STATUS    RESTARTS   AGE
  mynginx                             1/1     Running   0          28m
  nginx-deployment-645dcd4477-87twt   1/1     Running   0          5m58s
  nginx-deployment-645dcd4477-9xb9p   1/1     Running   0          5m58s
  nginx-deployment-645dcd4477-j9xt8   1/1     Running   0          5m58s
  ```

* 查看Deployment的副本数量 `kubectl get replicaSet`

  ```
  [root@k8s-master ~]# kubectl get replicaSet
  NAME                          DESIRED   CURRENT   READY   AGE
  nginx-deployment-645dcd4477   3         3         3       6m36s
  ```

* 手动扩缩容 `kubectl scale deploy 资源名称 --replicas=数量`

  ```
  # 将deployment/nginx-deployment的副本集扩充到5个
  [root@k8s-master ~]# kubectl scale deployment/nginx-deployment --replicas=5
  deployment.apps/nginx-deployment scaled
  # 查看扩缩后的Pod
  [root@k8s-master ~]# kubectl get pod
  NAME                                READY   STATUS    RESTARTS   AGE
  mynginx                             1/1     Running   0          36m
  nginx-deployment-645dcd4477-87twt   1/1     Running   0          13m
  nginx-deployment-645dcd4477-9xb9p   1/1     Running   0          13m
  nginx-deployment-645dcd4477-df828   1/1     Running   0          19s
  nginx-deployment-645dcd4477-j9xt8   1/1     Running   0          13m
  nginx-deployment-645dcd4477-t4cw5   1/1     Running   0          19s
  ```

* 自动扩缩容 `kubectl autoscale 资源名称 --min=最小pod数 --max=最大pod数 扩缩容条件 `

  > 扩缩容条件参考：https://github.com/kubernetes-sigs/metrics-server#readme

  ```
  #自动缩放，设置deployment/nginx-deployment为自动扩缩容，最小数量为3个pod，最大为10个pod，扩缩容的条件是所有pod的平均cpu使用率不超过75%
  [root@k8s-master ~]# kubectl autoscale deployment/nginx-deployment --min=3 --max=10 --cpu-percent=75 
  horizontalpodautoscaler.autoscaling/nginx-deployment autoscaled
  ```

* 滚动更新

  > 注意：在滚动更新的过程中会出现新旧服务共存在的状态

  ```
  # 设定deployment/nginx-deployment的镜像为nginx:1.23版本
  [root@k8s-master ~]# kubectl set image deployment/nginx-deployment nginx=nginx:1.23
  deployment.apps/nginx-deployment image updated
  #滚动更新状态
  kubectl rollout status deployment/nginx-deployment
  #查看过程
  kubectl get rs --watch
  ```

* 查看历史版本 `kubectl rollout history`

  ```
  [root@k8s-master ~]# kubectl rollout history deployment/nginx-deployment
  deployment.apps/nginx-deployment 
  REVISION  CHANGE-CAUSE
  1         <none>
  2         <none>
  ```

* 查看指定版本 ` kubectl rollout history deployment资源名称 --revision=版本号`

  ```
  [root@k8s-master ~]# kubectl rollout history deployment/nginx-deployment --revision=2
  deployment.apps/nginx-deployment with revision #2
  Pod Template:
    Labels:	app=nginx-deployment
  	pod-template-hash=5cf4667cdb
    Containers:
     nginx:
      Image:	nginx:1.23
      Port:	<none>
      Host Port:	<none>
      Environment:	<none>
      Mounts:	<none>
    Volumes:	<none>
    Node-Selectors:	<none>
    Tolerations:	<none>
  ```

* 回滚到历史版本 `kubectl rollout undo deployment资源名称 --to-revision=版本号`

  ```
  [root@k8s-master ~]# kubectl rollout undo deployment/nginx-deployment --to-revision=1
  deployment.apps/nginx-deployment rolled back
  ```

## Service

> Service会将将运行在一组Pod上的应用公开为网络服务，并为该组Pod提供相同的DNS名称，进行负载均衡。Kubernetes 为 Pod 提供分配了IP 地址，但IP地址可能会发生变化。Service会使集群内的容器可以通过service名称访问服务，而不需要担心Pod的IP发生变化。

![image.png](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202408241519868.png)

* 创建Service资源

  > ServiceType 取值
  >
  > - ClusterIP：将服务公开在集群内部。kubernetes会给服务分配一个集群内部的 IP，集群内的所有主机都可以通过这个Cluster-IP访问服务。集群内部的Pod可以通过service名称访问服务。
  > - [NodePort](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/#type-nodeport)：通过每个节点的主机IP 和静态端口（NodePort）暴露服务。 集群的外部主机可以使用节点IP和NodePort访问服务。
  > - [ExternalName](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/#externalname)：将集群外部的网络引入集群内部。
  > - [LoadBalancer](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/#loadbalancer)：使用云提供商的负载均衡器向外部暴露服务。 

  ```
  # 创建一个名称为nginx-service的Service，使用的资源为deployment/nginx-deployment，集群内部暴露的端口为8080，目标端口为80,这个服务只能在集群内部访问，无法在外部访问
  [root@k8s-master ~]#  kubectl expose deployment/nginx-deployment --name nginx-service --port=8080 --target-port=80
  service/nginx-service exposed
  
  # 创建一个名称为nginx-service的Service，使用的资源为deployment/nginx-deployment，对外暴露的端口为8081，目标端口为80
  [root@k8s-master ~]# kubectl expose deployment/nginx-deployment --name=nginx-outside --type=NodePort --port=8081 --target-port=80
  service/nginx-outside exposed
  ```

* 查看Service `kubectl get service`

  ```
  # nginx-outside暴露了两个端口，8081是集群内部访问的端口，31606是外部访问的端口（http://192.168.200.129:31606）
  [root@k8s-master ~]# kubectl get service
  NAME            TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
  kubernetes      ClusterIP   10.43.0.1      <none>        443/TCP    178m
  nginx-outside   NodePort    10.43.151.51   <none>        8081:31606/TCP   7s
  nginx-service   ClusterIP   10.43.21.154   <none>        8080/TCP   2m41s
  
  # 通过集群分配的ip+端口访问服务
  [root@k8s-master ~]# curl 10.43.21.154:8080
  <!DOCTYPE html>
  <html>
  <head>
  <title>Welcome to nginx!</title>
  <style>
  html { color-scheme: light dark; }
  body { width: 35em; margin: 0 auto;
  font-family: Tahoma, Verdana, Arial, sans-serif; }
  </style>
  </head>
  <body>
  <h1>Welcome to nginx!</h1>
  <p>If you see this page, the nginx web server is successfully installed and
  working. Further configuration is required.</p>
  
  <p>For online documentation and support please refer to
  <a href="http://nginx.org/">nginx.org</a>.<br/>
  Commercial support is available at
  <a href="http://nginx.com/">nginx.com</a>.</p>
  
  <p><em>Thank you for using nginx.</em></p>
  </body>
  </html>
  
  # 通过--rm参数创建一个一次性的pod(退出pod后会自动销毁)
  [root@k8s-master ~]# kubectl run test -it --image=nginx:1.22 --rm -- bash
  If you don't see a command prompt, try pressing enter.
  
  # 通过服务名称+端口进行访问
  root@test:/# curl nginx-service:8080
  <!DOCTYPE html>
  <html>
  <head>
  <title>Welcome to nginx!</title>
  <style>
  html { color-scheme: light dark; }
  body { width: 35em; margin: 0 auto;
  font-family: Tahoma, Verdana, Arial, sans-serif; }
  </style>
  </head>
  <body>
  <h1>Welcome to nginx!</h1>
  <p>If you see this page, the nginx web server is successfully installed and
  working. Further configuration is required.</p>
  
  <p>For online documentation and support please refer to
  <a href="http://nginx.org/">nginx.org</a>.<br/>
  Commercial support is available at
  <a href="http://nginx.com/">nginx.com</a>.</p>
  
  <p><em>Thank you for using nginx.</em></p>
  </body>
  </html>
  ```

* 查看service详细信息 `kubectl describe service 服务名称`

  ```
  [root@k8s-master ~]# kubectl describe service nginx-service
  Name:              nginx-service
  Namespace:         default
  Labels:            app=nginx-deployment
  Annotations:       <none>
  Selector:          app=nginx-deployment
  Type:              ClusterIP
  IP Family Policy:  SingleStack
  IP Families:       IPv4
  IP:                10.43.21.154
  IPs:               10.43.21.154
  Port:              <unset>  8080/TCP
  TargetPort:        80/TCP
  Endpoints:         10.42.0.11:80,10.42.1.8:80,10.42.1.9:80 + 2 more... # 负载均衡端点
  Session Affinity:  None
  Events:            <none>
  ```


## NameSpace

* 查看命名空间 `kubectl get namespace`

  > - `default` 默认的命名空间，不可删除，未指定命名空间的对象都会被分配到default中。
  > - `kube-system` Kubernetes 系统对象(控制平面和Node组件)所使用的命名空间。
  > - `kube-public` 自动创建的公共命名空间，所有用户（包括未经过身份验证的用户）都可以读取它。通常我们约定，将整个集群中公用的可见和可读的资源放在这个空间中。 
  > - `kube-node-lease`  [租约（Lease）](https://kubernetes.io/docs/reference/kubernetes-api/cluster-resources/lease-v1/)对象使用的命名空间。每个节点都有一个关联的 lease 对象，lease 是一种轻量级资源。lease对象通过发送[心跳](https://kubernetes.io/zh-cn/docs/concepts/architecture/nodes/#heartbeats)，检测集群中的每个节点是否发生故障。

  ```
  [root@k8s-master ~]# kubectl get namespace
  NAME              STATUS   AGE
  default           Active   3h19m
  kube-node-lease   Active   3h19m
  kube-public       Active   3h19m
  kube-system       Active   3h19m
  ```

* 创建命名空间 `kubectl create namespace dev`

  > 在创建Pod的时候可以使用 -n  参数指定命名空间

  ```
  [root@k8s-master ~]# kubectl create namespace dev
  namespace/dev created
  ```

* 删除命名空间

	>  删除命名空间时会同步删除该命名空间下的资源
	
	```
	[root@k8s-master ~]# kubectl delete namespace dev
	namespace "dev" deleted
	```
	
* 将dev设为当前命名空间，后续所有操作都在此命名空间下执行。

  ```
  kubectl config set-context $(kubectl config current-context) --namespace=dev
  ```

## 通过声明式对象配置
* 配置对象

	在创建的 Kubernetes 对象所对应的 `yaml`文件中，需要配置的字段如下：

    - `apiVersion` -  Kubernetes API 的版本
    - `kind` - 对象类别，例如`Pod`、`Deployment`、`Service`、`ReplicaSet`等
    - `metadata` - 描述对象的元数据，包括一个 name 字符串、UID 和可选的 namespace
    - `spec` - 对象的配置
  
* 栗子

  > 这个配置文件中的Pod资源通常不需要单独定义，因为Pod将由Deployment自动创建和管理。Pod资源在这里是为了演示配置文件的结构，但在实际使用中，Deployment足以管理Pod的生命周期。

  ```yaml
  apiVersion: v1 # api版本信息
  kind: Pod # 资源类型
  metadata:
    name: nginx
    labels:
      app.kubernetes.io/name: proxy # 定义一个key为name，value为proxy的标签
  spec:
    containers: # 下面为运行的容器列表
    - name: nginx # 容器名称
      image: nginx:1.22 # 镜像名称及版本号
      ports:
        - containerPort: 80 # 容器内部监听的端口
  ---
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: nginx-deployment-demo # deployment资源名称
    labels:
      app: nginx  # 定义一个key为app，value为nginx的标签
  spec:
    replicas: 3 # 指定副本数量为3个
    selector:
      matchLabels:
        app: nginx # 匹配标签key为app，value为nginx的所有资源
    template:
      metadata:
        labels:
          app: nginx # 定义一个key为app，value为nginx的标签
      spec:
        containers: # 下面为运行的容器列表
        - name: nginx # 容器名称
          image: nginx:1.22 # 镜像名称及版本号
          ports:
          - containerPort: 80 # 容器内部监听的端口
  ---
  apiVersion: v1
  kind: Service # 资源类型
  metadata:
    name: nginx-service-demo # 定义服务名称
  spec:
    selector:
      app: nginx # 匹配标签key为app，value为nginx的所有资源
    ports:
      - name: nginx-out-side 
        port: 80 # 集群内部暴露的端口
        nodePort: 31009 # 对外暴露的端口
        targetPort: 80 # 目标端口
    type: NodePort # 指定服务类型
  ```

* 通过配置文件创建Pod

  ```
  kubectl apply -f my-nginx.yaml
  ```

* 通过配置文件删除Pod

  ```
  kubectl delete -f my-nginx.yaml
  ```

  
