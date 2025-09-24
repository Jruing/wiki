# Kubernetes Service 学习笔记

## 简介

> **Service** 是 Kubernetes 中的一种资源对象，用于定义一组 Pod 的访问方式。Service 提供了一个稳定的访问入口，即使 Pod 的 IP 地址发生变化，也可以通过 Service 进行访问。Service 可以暴露 HTTP、TCP 等服务，通常用于负载均衡、访问控制等场景。

### Service 的类型

Kubernetes 提供了几种不同类型的 Service，具体的类型有：

1. **ClusterIP**：默认类型，暴露一个内部 IP，供集群内的其他服务访问。
2. **NodePort**：暴露一个端口，允许外部流量通过集群节点的 IP 和端口访问该服务。
3. **LoadBalancer**：通过云提供商的负载均衡器暴露服务，适用于公有云环境。
4. **ExternalName**：通过 DNS 名称将服务映射到外部服务。

---

## 创建 Service

### 方式一：使用 `kubectl expose` 命令

使用 `kubectl expose` 命令可以快速创建一个 Service：

```bash
kubectl expose pod <pod-name> --port=<port> --name=<service-name> --target-port=<target-port>
```

例如，暴露名为 `nginx` 的 Pod，端口为 80，服务名为 `nginx-service`：

```bash
kubectl expose pod nginx --port=80 --name=nginx-service --target-port=80
```

如果是暴露 Deployment 或 ReplicaSet，可以使用以下命令：

```bash
kubectl expose deployment <deployment-name> --port=<port> --name=<service-name> --target-port=<target-port>
```

### 方式二：使用 YAML 文件定义

通过 YAML 文件创建 Service，提供更灵活的配置方式。

#### ClusterIP 类型 Service（默认）

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service # 服务名称
spec:
  selector:
    app: my-app # 选择器，匹配的 Pod 标签
  ports:
    - protocol: TCP
      port: 80 # 服务暴露的端口
      targetPort: 8080 # 后端 Pod 端口
  type: ClusterIP # 默认类型
```

应用该 YAML 文件来创建 Service：

```bash
kubectl apply -f service-clusterip.yaml
```

#### NodePort 类型 Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-nodeport-service
spec:
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
      nodePort: 30001 # 外部访问端口
  type: NodePort # 设置为 NodePort 类型
```

应用该 YAML 文件：

```bash
kubectl apply -f service-nodeport.yaml
```

#### LoadBalancer 类型 Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-loadbalancer-service
spec:
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer # 设置为 LoadBalancer 类型
```

应用该 YAML 文件：

```bash
kubectl apply -f service-loadbalancer.yaml
```

---

## 查询 Service

### 查看所有 Service

可以使用以下命令查看当前命名空间中的所有 Service：

```bash
kubectl get services
```

### 查看特定 Service 的详情

查看某个 Service 的详细信息：

```bash
kubectl describe service <service-name>
```

例如，查看 `nginx-service` 的详细信息：

```bash
kubectl describe service nginx-service
```

---

## 更新 Service

虽然直接更新 Service 并不常见，但如果需要修改 Service 配置，可以通过修改 YAML 文件，然后重新应用它：

```bash
kubectl apply -f updated-service.yaml
```

如果想要修改某些特定的字段，比如端口或暴露类型，也可以使用 `kubectl expose` 来重新创建 Service。

---

## 删除 Service

### 方式一：根据 Service 名称删除

删除指定名称的 Service：

```bash
kubectl delete service <service-name>
```

例如，删除 `nginx-service`：

```bash
kubectl delete service nginx-service
```

### 方式二：根据 YAML 文件删除

如果是通过 YAML 文件创建的 Service，也可以使用文件删除：

```bash
kubectl delete -f service.yaml
```

---

## Service 的高级配置

### 使用 `selector` 和 `label` 实现动态发现

Service 通过 `selector` 来选择与其相关的 Pod。`selector` 使用 Pod 的标签进行匹配，确保请求流量路由到正确的 Pod。可以通过以下方式动态地选择和更新后端 Pod：

```yaml
spec:
  selector:
    app: my-app # 选择标签为 "app=my-app" 的 Pod
```

### Service 与 Pod 的关联

Service 可以暴露多个 Pod 服务，并通过 `targetPort` 指定后端容器的端口。例如，可以暴露一个 Deployment 中的多个 Pod 服务，保证高可用性。

### Health Checks（健康检查）

Kubernetes Service 会自动进行健康检查，确保流量只路由到健康的 Pod 上。如果使用了 `readinessProbe` 和 `livenessProbe`，Service 会根据这些探针来判断 Pod 是否处于健康状态。

---

## 小结

* **Service** 是 Kubernetes 中用于暴露 Pod 服务的资源对象，确保应用具有稳定的访问入口。
* **Service 类型**：`ClusterIP`（默认）、`NodePort`、`LoadBalancer` 和 `ExternalName`。
* **创建 Service**：可以通过 `kubectl expose` 命令或 YAML 文件创建。
* **查询与更新**：可以通过 `kubectl get services` 查看所有服务，并通过 YAML 文件更新配置。
* **删除 Service**：可以通过 `kubectl delete` 命令删除服务。
* **高级配置**：可以通过 `selector`、`label` 和健康检查来更好地管理 Pod 与 Service 的关系。
