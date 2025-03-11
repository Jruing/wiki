# 简介
> Namespace命名空间，用于项目隔离，一个命名空间代表一个项目，默认命名空间为default
# 创建Namespace
## 方式一
```
kubectl create namespace <命名空间名称>
```
## 方式二
```
apiVersion: v1
kind: Namespace # 资源类型
metadata:
  name: my-namespace # 命名空间名称
```
```
# 应用
kubectl apply -f create-namespace.yaml
```
# 查询Namespace
```
[root@VM-12-11-centos ~]# kubectl get namespace
NAME              STATUS   AGE
kube-system       Active   41d
kube-public       Active   41d
kube-node-lease   Active   41d
default           Active   41d
study             Active   20d
```
# 删除Namespace
```
kubectl delete namespace <命名空间名称>
```
```
kubectl delete -f create-namespace.yaml
```
# 修改默认工作命名空间
```
kubectl config set-context --current --namespace=my-namespace
```
# 强制删除
```
kubectl get ns kubernetes-dashboard -o json > kubernetes-dashboard.json
```
```
{
  "spec": {
    "finalizers": []
  }
}
```
```
kubectl replace --raw "/api/v1/namespaces/kubernetes-dashboard/finalize" -f kubernetes-dashboard.json
```