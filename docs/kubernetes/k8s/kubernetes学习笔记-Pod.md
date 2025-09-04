# 简介
> Pod是k8s中的最小资源单位

# 创建Pod
## 方式一
> 创建一个镜像为nginx，pod名称为my-pod的Pod
```
kubectl run my-pod --image=nginx
```
## 方式二
```
apiVersion: v1
kind: Pod # 资源类型
metadata:
  name: my-first-pod # 资源名称
  namespace: default # 命名空间名称
  labels:
    app: my-app 
spec:
  containers:
    - name: nginx-container # 容器名称
      image: nginx:latest # 镜像名称
      ports:
        - containerPort: 80 # 容器暴露端口
```
```
# 部署应用
kubectl apply -f demo-pod.yaml
```
# 查看Pod列表
```
kubectl get pod
```
# 查看Pod详情
```
kubectl describe pod pod名称
```
# 删除Pod
```
# 第一种，根据yaml文件删除
kubectl delete -f demo-pod.yaml

# 第二种，根据pod名称删除
kubectl delete pod pod名称
```