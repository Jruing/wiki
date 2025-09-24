## 简介

> Deployment 是 Kubernetes 中用于声明和管理一组副本（Pod）的控制器。它可以确保在集群中运行的 Pod 数量始终保持一致。使用 Deployment，可以轻松进行应用程序的滚动更新和回滚。

---

## 创建 Deployment

### 方式一：使用 `kubectl create` 命令

通过 `kubectl create` 命令直接创建一个 Deployment：

```bash
kubectl create deployment <deployment-name> --image=<image-name>
```

例如，创建一个名为 `nginx-deployment` 的 Deployment，镜像为 `nginx`：

```bash
kubectl create deployment nginx-deployment --image=nginx
```

该命令会创建一个 Deployment，并自动创建与之关联的 Pod。

### 方式二：使用 YAML 文件定义

可以通过 YAML 文件定义更为详细的 Deployment 配置：

```yaml
apiVersion: apps/v1
kind: Deployment # 资源类型
metadata:
  name: nginx-deployment # Deployment 名称
spec:
  replicas: 3 # Pod 副本数
  selector:
    matchLabels:
      app: nginx # 标签选择器
  template:
    metadata:
      labels:
        app: nginx # Pod 标签
    spec:
      containers:
        - name: nginx-container # 容器名称
          image: nginx:latest # 镜像名称
          ports:
            - containerPort: 80 # 容器暴露的端口
```

使用以下命令应用该 YAML 文件来创建 Deployment：

```bash
kubectl apply -f nginx-deployment.yaml
```

---

## 查看 Deployment 状态

### 获取 Deployment 列表

查看当前命名空间下的所有 Deployment：

```bash
kubectl get deployments
```

如果你想查看某个特定命名空间的 Deployment，可以使用以下命令：

```bash
kubectl get deployments -n <namespace-name>
```

### 查看 Deployment 详情

查看某个特定 Deployment 的详细信息：

```bash
kubectl describe deployment <deployment-name>
```

### 查看 Pod 状态

查看与某个 Deployment 关联的 Pod：

```bash
kubectl get pods -l app=<app-name>
```

例如，查看 `nginx` 应用的所有 Pod：

```bash
kubectl get pods -l app=nginx
```

---

## 更新 Deployment

### 滚动更新

更新 Deployment 时，Kubernetes 会自动进行滚动更新（滚动替换 Pod），以确保新版本的应用始终可以正常运行。

例如，如果你要更新 `nginx` 镜像为 `nginx:1.19`：

```bash
kubectl set image deployment/nginx-deployment nginx-container=nginx:1.19
```

K8s 会自动替换旧的 Pod，创建新的 Pod，直到所有副本都更新为新版本。

### 查看更新状态

你可以使用以下命令查看 Deployment 的更新状态：

```bash
kubectl rollout status deployment/nginx-deployment
```

### 回滚 Deployment

如果更新过程中发生问题，可以回滚到上一个版本：

```bash
kubectl rollout undo deployment/nginx-deployment
```

也可以回滚到指定的版本：

```bash
kubectl rollout undo deployment/nginx-deployment --to-revision=<revision-number>
```

---

## 删除 Deployment

### 方式一：根据 YAML 文件删除

如果 Deployment 是通过 YAML 文件创建的，可以使用以下命令删除：

```bash
kubectl delete -f nginx-deployment.yaml
```

### 方式二：根据 Deployment 名称删除

如果你知道 Deployment 的名称，可以直接通过名称删除：

```bash
kubectl delete deployment <deployment-name>
```

例如，删除名为 `nginx-deployment` 的 Deployment：

```bash
kubectl delete deployment nginx-deployment
```

---

## Deployment 的高级配置

### 设置副本数

你可以在创建 Deployment 时，指定副本数。副本数决定了 K8s 要运行多少个 Pod 实例来确保应用的高可用性。例如，以下配置会创建 3 个副本：

```yaml
spec:
  replicas: 3
```

### 配置资源限制

你可以为容器设置资源请求和限制，确保应用在运行时不会消耗过多资源。以下配置将设置容器的 CPU 和内存请求与限制：

```yaml
spec:
  containers:
    - name: nginx-container
      image: nginx
      resources:
        requests:
          memory: "64Mi"
          cpu: "250m"
        limits:
          memory: "128Mi"
          cpu: "500m"
```

* `requests`：容器启动时请求的最低资源量。
* `limits`：容器能使用的最大资源量。

### 配置环境变量

你可以为容器设置环境变量，这些环境变量会在容器启动时传递给应用。例如：

```yaml
spec:
  containers:
    - name: nginx-container
      image: nginx
      env:
        - name: ENVIRONMENT
          value: "production"
```

### 配置健康检查

K8s 支持容器的健康检查，以确保容器处于健康状态。你可以配置 `livenessProbe` 和 `readinessProbe` 来检测容器的存活性和就绪状态。例如：

```yaml
spec:
  containers:
    - name: nginx-container
      image: nginx
      livenessProbe:
        httpGet:
          path: /healthz
          port: 80
        initialDelaySeconds: 3
        periodSeconds: 3
      readinessProbe:
        httpGet:
          path: /readiness
          port: 80
        initialDelaySeconds: 5
        periodSeconds: 5
```

---

# 小结

* **Deployment** 是 K8s 中用于管理一组副本 Pod 的控制器，能够实现应用的自动滚动更新、回滚和高可用性。
* **创建 Deployment** 可以通过 `kubectl create deployment` 命令或者通过定义 YAML 文件来实现。
* **管理 Deployment** 可以通过 `kubectl rollout` 命令来实现滚动更新、查看更新状态和回滚。
* **删除 Deployment** 可以通过 `kubectl delete` 命令来删除，支持根据文件或名称删除。
* **高级配置** 包括副本数、资源限制、环境变量、健康检查等。
