# 安装
```
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