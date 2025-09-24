# 安装
```
# 国内用户
curl -sfL https://rancher-mirror.rancher.cn/k3s/k3s-install.sh | INSTALL_K3S_MIRROR=cn sh -
```
# 获取token
```
cat /var/lib/rancher/k3s/server/node-token
```
# 其他节点加入集群
```
curl -sfL https://rancher-mirror.rancher.cn/k3s/k3s-install.sh | INSTALL_K3S_MIRROR=cn K3S_URL=https://替换成服务节点ip:6443 K3S_TOKEN=替换成上面获取的token sh -
```
# 查询节点
> 获取详细信息：kubectl get nodes -o wide
```
[root@VM-12-11-centos ~]# kubectl get nodes
NAME              STATUS   ROLES                  AGE   VERSION
vm-12-11-centos   Ready    control-plane,master   41d   v1.28.2+k3s1
```
# 其他环境变量
```
Environment Variable	        Description
INSTALL_K3S_SKIP_DOWNLOAD	如果设置为 "true "将不会下载 K3s 的哈希值或二进制。
INSTALL_K3S_SYMLINK	        默认情况下，如果路径中不存在命令，将为 kubectl、crictl 和 ctr 二进制文件创建符号链接。如果设置为'skip'将不会创建符号链接，而'force'将覆盖。
INSTALL_K3S_SKIP_ENABLE	        如果设置为 "true"，将不启用或启动 K3s 服务。
INSTALL_K3S_SKIP_START	        如果设置为 "true "将不会启动 K3s 服务。
INSTALL_K3S_VERSION	        从 Github 下载 K3s 的版本。如果没有指定，将尝试从"stable"频道下载。
INSTALL_K3S_BIN_DIR	        安装 K3s 二进制文件、链接和卸载脚本的目录，或者使用/usr/local/bin作为默认目录。
INSTALL_K3S_BIN_DIR_READ_ONLY	如果设置为 true 将不会把文件写入INSTALL_K3S_BIN_DIR，强制设置INSTALL_K3S_SKIP_DOWNLOAD=true。
INSTALL_K3S_SYSTEMD_DIR	        安装 systemd 服务和环境文件的目录，或者使用/etc/systemd/system作为默认目录。
INSTALL_K3S_EXEC	        带有标志的命令，用于在服务中启动 K3s。如果未指定命令，并且设置了K3S_URL，它将默认为“agent”。如果未设置K3S_URL，它将默认为“server”。
INSTALL_K3S_NAME	        要创建的 systemd 服务名称，如果以服务器方式运行 k3s，则默认为'k3s'；如果以 agent 方式运行 k3s，则默认为'k3s-agent'。如果指定了服务名，则服务名将以'k3s-'为前缀。
INSTALL_K3S_TYPE	        要创建的 systemd 服务类型，如果没有指定，将默认使用 K3s exec 命令。
INSTALL_K3S_SELINUX_WARN	如果设置为 true，则在没有找到 k3s-selinux 策略的情况下将继续。
INSTALL_K3S_SKIP_SELINUX_RPM	如果设置为 "true "将跳过 k3s RPM 的自动安装。
INSTALL_K3S_CHANNEL_URL	        用于获取 K3s 下载网址的频道 URL。默认为 https://update.k3s.io/v1-release/channels 。
INSTALL_K3S_CHANNEL	        用于获取 K3s 下载 URL 的通道。默认值为 "stable"。选项包括：stable, latest, testing。
K3S_CONFIG_FILE	                指定配置文件的位置。默认目录为/etc/rancher/k3s/config.yaml。
K3S_TOKEN	                用于将 server 或 agent 加入集群的共享 secret。
K3S_TOKEN_FILE	                指定 cluster-secret,token 的文件目录。
```