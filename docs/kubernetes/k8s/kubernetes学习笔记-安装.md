# 安装 K3s

### 国内用户安装

```bash
# 国内用户
curl -sfL https://rancher-mirror.rancher.cn/k3s/k3s-install.sh | INSTALL_K3S_MIRROR=cn sh -
```

### 获取 K3s Token

在 K3s 的主节点上执行以下命令获取 token：

```bash
cat /var/lib/rancher/k3s/server/node-token
```

### 添加其他节点到集群

在其他节点上，执行以下命令加入集群。替换其中的 `K3S_URL` 和 `K3S_TOKEN` 为主节点的 IP 地址和从上面获取的 token。

```bash
curl -sfL https://rancher-mirror.rancher.cn/k3s/k3s-install.sh | INSTALL_K3S_MIRROR=cn K3S_URL=https://<主节点IP>:6443 K3S_TOKEN=<获取的Token> sh -
```

**注意：**

* 每台计算机必须具有唯一的主机名。如果计算机没有唯一的主机名，请设置 `K3S_NODE_NAME` 环境变量，为每个节点指定有效且唯一的主机名。

---

# 查询集群节点

你可以通过以下命令查询节点的状态与信息：

```bash
kubectl get nodes -o wide
```

例如，返回的结果如下：

```bash
[root@VM-12-11-centos ~]# kubectl get nodes
NAME              STATUS   ROLES                  AGE   VERSION
vm-12-11-centos   Ready    control-plane,master   41d   v1.28.2+k3s1
```

---

# 其他环境变量配置

K3s 安装时，支持以下环境变量进行进一步配置：

| 环境变量                            | 描述                                                                                 |
| ------------------------------- | ---------------------------------------------------------------------------------- |
| `INSTALL_K3S_SKIP_DOWNLOAD`     | 如果设置为 `true`，将跳过下载 K3s 的哈希值或二进制文件。                                                 |
| `INSTALL_K3S_SYMLINK`           | 如果设置为 `skip`，则不创建符号链接；如果设置为 `force`，则强制覆盖符号链接。                                     |
| `INSTALL_K3S_SKIP_ENABLE`       | 如果设置为 `true`，将不会启用或启动 K3s 服务。                                                      |
| `INSTALL_K3S_SKIP_START`        | 如果设置为 `true`，将不会启动 K3s 服务。                                                         |
| `INSTALL_K3S_VERSION`           | 指定从 GitHub 下载 K3s 的版本，默认下载 `stable` 版本。                                            |
| `INSTALL_K3S_BIN_DIR`           | 指定安装 K3s 二进制文件、链接和卸载脚本的目录，默认是 `/usr/local/bin`。                                    |
| `INSTALL_K3S_BIN_DIR_READ_ONLY` | 如果设置为 `true`，不会将文件写入 `INSTALL_K3S_BIN_DIR`，并强制设置 `INSTALL_K3S_SKIP_DOWNLOAD=true`。 |
| `INSTALL_K3S_SYSTEMD_DIR`       | 指定安装 systemd 服务和环境文件的目录，默认是 `/etc/systemd/system`。                                 |
| `INSTALL_K3S_EXEC`              | 启动 K3s 服务时使用的命令，默认情况下服务器为 `server`，代理为 `agent`。                                    |
| `INSTALL_K3S_NAME`              | 要创建的 systemd 服务名称。如果以服务器方式运行，默认为 `k3s`；如果以代理方式运行，默认为 `k3s-agent`。                  |
| `INSTALL_K3S_TYPE`              | 要创建的 systemd 服务类型。默认使用 K3s 执行命令。                                                   |
| `INSTALL_K3S_SELINUX_WARN`      | 如果设置为 `true`，在没有找到 `k3s-selinux` 策略的情况下继续安装。                                       |
| `INSTALL_K3S_SKIP_SELINUX_RPM`  | 如果设置为 `true`，跳过自动安装 `k3s-selinux` RPM 包。                                           |
| `INSTALL_K3S_CHANNEL_URL`       | 获取 K3s 下载 URL 的频道 URL，默认值为 `https://update.k3s.io/v1-release/channels`。            |
| `INSTALL_K3S_CHANNEL`           | 用于获取 K3s 下载 URL 的频道。默认值为 `stable`，可选值包括：`stable`, `latest`, `testing`。             |
| `K3S_CONFIG_FILE`               | 指定配置文件的位置，默认是 `/etc/rancher/k3s/config.yaml`。                                      |
| `K3S_TOKEN`                     | 用于将 server 或 agent 加入集群的共享 token。                                                  |
| `K3S_TOKEN_FILE`                | 指定存储 cluster-secret 和 token 的文件路径。                                                 |

---

# 补充内容

* **K3s 安装时的权限问题**：
  如果在安装过程中遇到权限问题，可以使用 `sudo` 来提高权限。例如：

  ```bash
  sudo curl -sfL https://rancher-mirror.rancher.cn/k3s/k3s-install.sh | INSTALL_K3S_MIRROR=cn sh -
  ```

* **K3s 安装后的自动启动服务**：
  默认情况下，K3s 会将服务注册为 `systemd` 服务，确保系统启动时 K3s 自动启动。如果需要关闭自动启动，可以设置 `INSTALL_K3S_SKIP_ENABLE=true`。

* **通过 Helm 部署应用**：
  如果需要使用 Helm 来部署应用，可以首先安装 Helm：

  ```bash
  curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
  ```

  然后初始化 Helm，并使用 Helm 部署应用到 K3s 集群。
