# 简介
> ConfigMap 是一种 API 对象，用于存储配置信息，比如配置文件、环境变量或命令行参数
# 创建
## 方式一: Key/Value
```
kubectl create configmap my-config --from-literal=key1=value1 --from-literal=key2=value2
```
## 方式二: yaml文件
```
kubectl create configmap my-config --from-file=app-config.properties
```
## 单行
```
apiVersion: v1
kind: ConfigMap # 资源类型
metadata:
  name: my-config # key
  namespace: default # 命名空间名称
data: # value
  key1: value1
  key2: value2
```
```
kubectl apply -f create-configmap.yaml
```
## 多行
```
apiVersion: v1
kind: ConfigMap # 资源类型
metadata:
  name: my-config-multiline # key
  namespace: default // 命名空间名称
data:  # value
  config.properties: |
    key1=value1
    key2=value2
    key3=value3
  another-file.txt: |
    Line 1 of the file
    Line 2 of the file
```
```
kubectl apply -f create-configmap.yaml
```
# 删除ConfigMap
## 方式一
```
kubectl delete configmap my-config
```
## 方式二
```
kubectl delete -f create-configmap.yaml
```