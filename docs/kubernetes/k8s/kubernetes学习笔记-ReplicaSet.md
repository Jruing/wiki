# 简介
> ReplicaSet用来确保指定数量的 Pod 副本在任何时间点都在运行的控制器。它会确保即使某些 Pod 出现故障或被删除，系统也会创建新的 Pod 来替代它们，从而维持一定数量的 Pod 副本
# 创建ReplicaSet
## 方式一
```
kubectl create replicaset my-replicaset --image=nginx --replicas=3
```
## 方式二
```
apiVersion: apps/v1
kind: ReplicaSet # 资源类型
metadata:
  name: my-replicaset # 副本名称
spec:
  replicas: 3 # 副本数量
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx-container
          image: nginx
```
```
# 应用
kubectl apply -f create-replicaset.yaml
```
# 查询ReplicaSet
```
[root@VM-12-11-centos ~]# kubectl get replicasets -n study
NAME                     DESIRED   CURRENT   READY   AGE
nginx-5dcfbfcdb6         1         1         1       17d
```
# 删除ReplicaSet
```
kubectl delete replicaset my-replicaset
```
```
kubectl delete -f create-namespace.yaml
```
# ReplicaSet优点
ReplicaSet 主要用于保证系统中的 Pod 副本数目稳定。它有以下优势：
- 自动恢复：如果某个 Pod 宕机或被删除，ReplicaSet 会自动创建新的 Pod 来替代。
- 负载均衡：可以通过 ReplicaSet 来确保某个服务的可用性和负载均衡，确保多个副本在不同节点上分布。
ReplicaSet 常常与 Deployment 一起使用。Deployment 会在背后管理 ReplicaSet，提供更高级的功能，比如滚动更新、回滚等。