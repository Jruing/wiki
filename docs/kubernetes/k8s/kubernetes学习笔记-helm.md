## 简介

> **Helm** 是 Kubernetes 的包管理器，类似于 Linux 下的 `apt` 或 `yum`，可以方便地管理 Kubernetes 中的应用程序。Helm 通过 **charts**（预打包的 Kubernetes 资源集合）来实现应用的安装、升级、版本控制等。

---

## 安装 Helm

### 手动安装

#### 1. 下载 Helm 安装脚本

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
```

#### 2. 赋予安装脚本执行权限

```bash
chmod 700 get_helm.sh
```

#### 3. 执行安装脚本

```bash
./get_helm.sh
```

或者直接执行：

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

---

## 添加 Helm Chart 仓库

Helm 支持多个仓库，以下是添加常用仓库的命令：

```bash
# 添加 Bitnami 仓库
helm repo add bitnami https://charts.bitnami.com/bitnami

# 国内常用的 Helm 仓库
helm repo add aliyuncs https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts
helm repo add kaiyuanshe http://mirror.kaiyuanshe.cn/kubernetes/charts
helm repo add azure http://mirror.azure.cn/kubernetes/charts
helm repo add dandydev https://dandydeveloper.github.io/charts
```

---

## 更新 Helm 仓库

通过以下命令更新所有已添加的 Helm 仓库：

```bash
helm repo update
```

---

## 查看已添加的 Helm 仓库

查看当前 Helm 仓库列表：

```bash
helm repo list
```

---

## 删除 Helm 仓库

删除指定仓库：

```bash
helm repo remove <repo-name>
```

例如，删除 `bitnami` 仓库：

```bash
helm repo remove bitnami
```

---

## 查看 Helm Charts 列表

```bash
helm list
```

---

## 全网仓库查询

通过 `helm search hub` 从 Artifact Hub 查询 Helm Charts：

```bash
helm search hub mysql
```

---

## 从本地仓库查询

查询已添加的本地 Helm 仓库中的 Charts：

```bash
helm search repo mysql
```

---

## 拉取 Helm Chart 包

拉取指定版本的 Helm Chart 包：

```bash
helm pull azure/mysql --version 0.3.5
```

---

## 安装 Helm Chart

安装 Chart 时，可以通过 `--set` 参数传递自定义值，或直接使用 `helm install` 安装：

### 示例 1：指定 `release` 名称安装

```bash
helm install test-mysql azure/mysql
```

### 示例 2：让 Helm 随机生成 `release` 名称

```bash
helm install aliyuncs/mysql --generate-name
```

### 示例 3：指定命名空间安装

```bash
helm install aliyuncs/mysql --namespace my-namespace
```

### 示例 4：若命名空间不存在，则创建新的命名空间

```bash
helm install aliyuncs/mysql --namespace my-namespace --create-namespace
```

---

## 卸载 Helm Chart

```bash
helm uninstall <release-name>
```

例如，卸载 `test-mysql`：

```bash
helm uninstall test-mysql
```

---

## 查询 Helm Chart 状态

```bash
helm status <release-name>
```

例如，查询 `my-nginx` 状态：

```bash
helm status my-nginx
```

---

## 自定义 Helm Chart

### 查询 Chart 的可配置项

使用 `helm show values` 查看某个 Chart 的默认配置项：

```bash
helm show values azure/mysql
```

该命令会列出该 Chart 支持的所有配置项，如：

* MySQL 镜像版本、root 密码、数据库名称等。
* 持久化配置、资源请求和限制等。

### 修改配置并安装

可以通过 `--set` 参数覆盖 Chart 中的默认值：

```bash
helm install --set mysqlRootPassword=test1234,mysqlDatabase=testdb,service.nodePort=32001,service.type=NodePort test-mysql azure/mysql
```

在上述命令中，`mysqlRootPassword`、`mysqlDatabase` 和 `service.nodePort` 是需要自定义的配置项。

---

## 更新 Helm Chart

```bash
helm upgrade <release-name> --set <key1>=<value1>,<key2>=<value2> <chart-name>
```

例如，更新 `test-mysql` 的 `mysqlRootPassword`：

```bash
helm upgrade test-mysql --set mysqlRootPassword=test1234 azure/mysql
```

---

## 查看 Helm Chart 修订历史

查看 `release` 的修订历史：

```bash
helm history <release-name>
```

例如，查看 `test-mysql` 的修订历史：

```bash
helm history test-mysql
```

---

## 回滚 Helm Chart

回滚到指定版本：

```bash
helm rollback <release-name> <revision-number>
```

例如，回滚 `test-mysql` 到第 1 版本：

```bash
helm rollback test-mysql 1
```

---

## 查看 Helm 帮助信息

查看 Helm 的帮助信息：

```bash
helm get -h
```

---

## 常见问题及解决方案

### 1. K3s 使用 Helm 出现连接失败

```bash
# 错误信息
Error: Kubernetes cluster unreachable: Get "http://127.0.0.1:8080/version": read tcp 127.0.0.1:45436->127.0.0.1:8080: read: connection reset by peer

# 解决方案：临时
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

# 解决方案：永久（推荐，否则安装 Chart 时部分功能可能没有权限）
vi /etc/profile
# 最后一行写入
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
# 激活
source /etc/profile
```

---

### 2. Helm 安装 Chart 失败

```bash
# 错误信息
Error: INSTALLATION FAILED: unable to build kubernetes objects from release manifest: resource mapping not found for name: "test-mysql-mysql" namespace: "" from "": no matches for kind "Deployment" in version "extensions/v1beta1"

# 解决方案：换一个仓库的 Chart 或使用 `stable` 仓库中的 Chart
```

---

## 小结

* **Helm** 是 Kubernetes 中的包管理器，便于安装、管理、升级、回滚等操作。
* **Charts** 是 Helm 使用的包，包含 Kubernetes 资源的所有定义，支持自定义配置。
* 通过 `helm repo` 可以管理 Helm 仓库，`helm install` 用于安装 Chart，`helm upgrade` 和 `helm rollback` 用于更新和回滚。
* 使用 `helm uninstall` 卸载已安装的 Chart。
* 遇到连接问题时，需要确保配置正确，尤其是 `KUBECONFIG` 环境变量的设置。
