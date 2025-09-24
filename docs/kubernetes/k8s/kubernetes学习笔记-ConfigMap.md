## 简介

> **ConfigMap** 是 Kubernetes 中的一个 API 对象，用于存储非敏感的配置信息，比如配置文件、环境变量、命令行参数等。它帮助将配置信息与应用程序代码分离，使得应用的配置更加灵活，便于管理和更新。

---

## 创建 ConfigMap

### 方式一：通过 `--from-literal` 创建

使用 `kubectl create configmap` 命令通过指定键值对的方式创建 ConfigMap：

```bash
kubectl create configmap my-config --from-literal=key1=value1 --from-literal=key2=value2
```

这将创建一个名为 `my-config` 的 ConfigMap，其中包含 `key1=value1` 和 `key2=value2`。

### 方式二：通过 `--from-file` 创建

你也可以将配置文件创建为 ConfigMap，命令如下：

```bash
kubectl create configmap my-config --from-file=app-config.properties
```

这将创建一个 ConfigMap，其中 `app-config.properties` 文件的内容作为 ConfigMap 的数据。

### 方式三：通过 YAML 文件创建

你可以使用 YAML 文件来定义 ConfigMap，使其更加灵活并支持更多配置。

#### 单行配置

```yaml
apiVersion: v1
kind: ConfigMap # 资源类型
metadata:
  name: my-config # ConfigMap 名称
  namespace: default # 命名空间名称
data: # 配置数据
  key1: value1
  key2: value2
```

使用以下命令应用该 YAML 文件：

```bash
kubectl apply -f create-configmap.yaml
```

#### 多行配置

如果配置文件中包含多行内容，可以使用 `|` 来表示多行数据：

```yaml
apiVersion: v1
kind: ConfigMap # 资源类型
metadata:
  name: my-config-multiline # ConfigMap 名称
  namespace: default # 命名空间名称
data: # 配置数据
  config.properties: |
    key1=value1
    key2=value2
    key3=value3
  another-file.txt: |
    Line 1 of the file
    Line 2 of the file
```

使用以下命令应用该 YAML 文件：

```bash
kubectl apply -f create-configmap.yaml
```

`|` 表示多行数据，保留换行符，使得配置更加符合格式。

---

## 删除 ConfigMap

### 方式一：根据名称删除

如果你知道 ConfigMap 的名称，可以直接删除：

```bash
kubectl delete configmap my-config
```

### 方式二：根据 YAML 文件删除

如果是通过 YAML 文件创建的 ConfigMap，可以使用以下命令删除：

```bash
kubectl delete -f create-configmap.yaml
```

---

## 使用 ConfigMap

### 将 ConfigMap 挂载为文件

你可以将 ConfigMap 挂载到 Pod 中作为文件，配置文件中的每个键值对将会成为 Pod 中的文件。以下是 YAML 文件示例：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: nginx
      volumeMounts:
        - name: config-volume
          mountPath: /etc/config
  volumes:
    - name: config-volume
      configMap:
        name: my-config
```

在这个示例中，`my-config` ConfigMap 被挂载到 `/etc/config` 目录中，ConfigMap 中的键 `key1` 和 `key2` 将会成为文件，内容分别是 `value1` 和 `value2`。

### 将 ConfigMap 注入为环境变量

你也可以将 ConfigMap 的内容作为环境变量注入到容器中：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: nginx
      envFrom:
        - configMapRef:
            name: my-config
```

在这个示例中，`my-config` ConfigMap 中的所有键值对将会被注入为环境变量。环境变量的名称是 ConfigMap 中的键，环境变量的值是 ConfigMap 中的值。

---

## 配置与 Pod 的结合使用

ConfigMap 可以帮助配置应用程序而无需将配置信息硬编码在容器镜像中。通过将 ConfigMap 挂载为文件或注入环境变量，应用可以灵活地根据不同环境和配置做出调整。

* **挂载为文件**：适用于应用读取配置文件的场景。
* **作为环境变量**：适用于应用以环境变量方式读取配置的场景。

---

## 小结

* **ConfigMap** 用于存储非敏感的配置信息，可以在 Kubernetes 中灵活使用。
* **创建 ConfigMap** 可以通过命令 `kubectl create configmap` 或者使用 YAML 文件。
* **删除 ConfigMap** 可以通过 `kubectl delete` 命令实现。
* ConfigMap 可用于将配置信息注入到 Pod 中，通过挂载文件或环境变量的方式，简化配置管理。
