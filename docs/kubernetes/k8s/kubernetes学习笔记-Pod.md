# 简介

> Pod 是 Kubernetes (K8s) 中最小的部署单元，包含一个或多个容器，运行在同一主机上的资源共享环境中。

---

# 创建 Pod

### 方式一：使用 `kubectl run` 命令

创建一个镜像为 `nginx`，Pod 名称为 `my-pod` 的 Pod：

```bash
kubectl run my-pod --image=nginx
```

此命令会创建一个新的 Pod，Pod 名称为 `my-pod`，并使用 `nginx` 镜像来创建容器。

### 方式二：使用 YAML 文件定义

通过 YAML 文件创建 Pod，更适合需要更复杂配置的场景。

```yaml
apiVersion: v1
kind: Pod # 资源类型
metadata:
  name: my-first-pod # Pod 名称
  namespace: default # 命名空间名称
  labels:
    app: my-app # 标签
spec:
  containers:
    - name: nginx-container # 容器名称
      image: nginx:latest # 镜像名称
      ports:
        - containerPort: 80 # 容器暴露端口
```

通过以下命令应用这个 YAML 文件来部署 Pod：

```bash
kubectl apply -f demo-pod.yaml
```

---

# 查看 Pod 状态

### 查看 Pod 列表

获取当前命名空间下的所有 Pod：

```bash
kubectl get pod
```

如果你希望查看某个特定命名空间的 Pod，可以使用以下命令：

```bash
kubectl get pod -n <namespace-name>
```

### 查看 Pod 详情

查看指定 Pod 的详细信息：

```bash
kubectl describe pod <pod-name>
```

---

# 删除 Pod

### 方式一：根据 YAML 文件删除

如果你使用 YAML 文件创建 Pod，可以使用以下命令删除：

```bash
kubectl delete -f demo-pod.yaml
```

### 方式二：根据 Pod 名称删除

如果你希望删除特定的 Pod，可以通过 Pod 名称来删除：

```bash
kubectl delete pod <pod-name>
```

---

# 删除 Pod 状态为 Terminating

有时，Pod 可能会处于 `Terminating` 状态，并无法正常删除。可以尝试以下方法强制删除。

### 方法 1：使用 `--force` 和 `--grace-period=0`

```bash
kubectl delete pod <pod-name> -n <namespace-name> --force --grace-period=0
```

### 方法 2：修改 Pod 的 finalizer

通过 patch 操作删除 Pod 的 finalizer，使其跳过清理步骤并强制删除：

```bash
kubectl patch pod <pod-name> -n <namespace-name> -p '{"metadata":{"finalizers":null}}'
```

---

# 补充内容

* **Pod 和容器**：Pod 内可以包含多个容器，这些容器共享网络和存储资源。如果需要运行多个紧密耦合的容器（例如，日志收集器与应用容器），可以将它们放在同一个 Pod 内。

* **Pod 的生命周期**：Pod 本身是临时的，通常不用于长期存储数据。在 K8s 中，Pod 可能会被调度到不同的节点上，节点故障时也会重新调度 Pod。为持久化存储，通常会使用持久卷（Persistent Volumes）和持久卷声明（Persistent Volume Claims）。

* **Pod 的调度与资源限制**：

  * 可以为 Pod 定义资源请求和限制，来保证其运行所需的 CPU 和内存。

    例如，以下 YAML 文件配置了 CPU 和内存的请求与限制：

```yaml
apiVersion: v1
kind: Pod
metadata:
name: my-pod
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

  * `requests`：指定容器启动时请求的最低资源量。

  * `limits`：指定容器能使用的最大资源量。

* **Pod 的重启策略**：Pod 可以配置不同的重启策略，常见的有：

  * `Always`：每次 Pod 失败时都会重启容器。
  * `OnFailure`：容器失败时会重启，但正常退出时不会重启。
  * `Never`：不会重启容器，容器失败后就会被标记为 `Failed` 状态。

  示例 YAML 配置重启策略：
```yaml
apiVersion: v1
kind: Pod
metadata:
name: my-pod
spec:
restartPolicy: OnFailure
containers:
  - name: nginx-container
    image: nginx
```
