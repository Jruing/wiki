
## 简介

> **Namespace** 是 Kubernetes 中用于资源隔离的机制。每个 Namespace 代表一个独立的项目或环境，能够将同一集群中的不同项目进行隔离。默认的 Namespace 是 `default`。

---

## 创建 Namespace

### 方式一：使用 `kubectl create namespace` 命令

直接使用 `kubectl` 命令创建一个新的 Namespace：

```bash
kubectl create namespace <namespace-name>
```

例如，创建一个名为 `study` 的 Namespace：

```bash
kubectl create namespace study
```

### 方式二：通过 YAML 文件创建

也可以通过 YAML 文件定义 Namespace，然后使用 `kubectl apply` 命令进行创建：

```yaml
apiVersion: v1
kind: Namespace # 资源类型
metadata:
  name: my-namespace # Namespace 名称
```

应用该 YAML 文件创建 Namespace：

```bash
kubectl apply -f create-namespace.yaml
```

---

## 查询 Namespace

要查看当前集群中的所有 Namespace，可以使用以下命令：

```bash
kubectl get namespace
```

例如，返回的结果可能是：

```bash
NAME              STATUS   AGE
kube-system       Active   41d
kube-public       Active   41d
kube-node-lease   Active   41d
default           Active   41d
study             Active   20d
```

此命令会显示每个 Namespace 的名称、状态和创建时间。

---

## 删除 Namespace

### 方式一：根据命名空间名称删除

使用以下命令删除指定的 Namespace：

```bash
kubectl delete namespace <namespace-name>
```

例如，删除 `study` Namespace：

```bash
kubectl delete namespace study
```

### 方式二：根据 YAML 文件删除

如果是通过 YAML 文件创建的 Namespace，也可以使用该文件删除：

```bash
kubectl delete -f create-namespace.yaml
```

---

## 修改默认工作命名空间

在 Kubernetes 中，默认的工作命名空间是 `default`。如果你希望修改当前上下文的工作命名空间，可以使用以下命令：

```bash
kubectl config set-context --current --namespace=<namespace-name>
```

例如，切换当前上下文的工作命名空间为 `study`：

```bash
kubectl config set-context --current --namespace=study
```

切换后，所有后续的 `kubectl` 命令都将默认操作 `study` 命名空间中的资源。

---

## 强制删除 Namespace

有时，命名空间在删除时可能会进入 `Terminating` 状态，无法正常删除。此时，你可以通过以下步骤强制删除该 Namespace。

### 步骤 1：获取 Namespace 的 JSON 配置

首先，使用 `kubectl get ns` 获取 Namespace 的配置并保存为 JSON 文件：

```bash
kubectl get ns <namespace-name> -o json > <namespace-name>.json
```

例如，获取 `kubernetes-dashboard` 命名空间的 JSON 配置：

```bash
kubectl get ns kubernetes-dashboard -o json > kubernetes-dashboard.json
```

### 步骤 2：修改 JSON 配置，清除 finalizers

编辑生成的 JSON 文件，将 `spec.finalizers` 设为空数组：

```json
{
  "spec": {
    "finalizers": []
  }
}
```

### 步骤 3：强制删除 Namespace

使用 `kubectl replace` 命令强制删除命名空间：

```bash
kubectl replace --raw "/api/v1/namespaces/kubernetes-dashboard/finalize" -f kubernetes-dashboard.json
```

这将清除 `finalizers`，并强制删除 `kubernetes-dashboard` 命名空间。

---

## 小结

* **Namespace** 提供了 Kubernetes 中的资源隔离，适用于多租户环境或多个项目的管理。
* **创建 Namespace** 可以通过命令 `kubectl create namespace` 或者使用 YAML 文件。
* **查询 Namespace** 可以使用 `kubectl get namespace` 查看所有 Namespace。
* **删除 Namespace** 可以通过命名空间名称或 YAML 文件删除，删除过程中如果遇到问题，可以通过强制删除解决。
* **修改默认工作命名空间** 通过 `kubectl config set-context` 命令设置当前上下文的命名空间。
