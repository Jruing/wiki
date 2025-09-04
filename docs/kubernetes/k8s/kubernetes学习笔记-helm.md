# Helm 学习笔记
> Helm 是 Kubernetes 的包管理器
## 手动执行
```
# 下载脚本
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
# 赋权
chmod 700 get_helm.sh
# 执行
./get_helm.sh
直接执行
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```
## 添加Helm chart仓库

> bitnami 仓库名称，可以自定义，https://charts.bitnami.com/bitnami 仓库地址
```
helm repo add bitnami https://charts.bitnami.com/bitnami
# 下面为国内常用的几个charts仓库
helm repo add aliyuncs https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts
helm repo add kaiyuanshe http://mirror.kaiyuanshe.cn/kubernetes/charts
helm repo add azure http://mirror.azure.cn/kubernetes/charts
helm repo add dandydev https://dandydeveloper.github.io/charts
```
## 更新chart仓库列表
```
helm repo update
```
## 查看chart仓库列表
```
helm repo list
```
## 删除仓库
```
helm repo remove bitnami
```
## 查看chart列表
```
helm list
```
## 全网仓库查询
> 从Artifact Hub中查询，他会列出所有mysql的charts
```
helm search hub mysql
```
## 从本地仓库查询
> 从安装的repo中查找，仅限于本地已安装的repo
```
helm search repo mysql
```
## 拉取chart包
```
helm pull azure/mysql --version 0.3.5
```
## 安装chart
>test-mysql 为自定义的release名称, aliyuncs/mysql 为charts名称
```
helm install test-mysql azure/mysql
# 让chart随机生成release
helm install aliyuncs/mysql --generate-name
# 指定命名空间名称
helm install aliyuncs/mysq --namespace my-namespace
# 若命名空间不存在，则创建新的命名空间
helm install aliyuncs/mysq --namespace my-namespace --create-namespace
```
## 卸载chart
```
helm uninstall <chart名称>
```
## 查询状态
```
helm status my-nginx
```
## 自定义chart
### 查询chart的可配置项
```
[root@VM-12-11-centos k8s_yaml]# helm show values azure/mysql
## mysql image version
## ref: https://hub.docker.com/r/library/mysql/tags/
##
image: "mysql"
imageTag: "5.7.14"

## Specify password for root user
##
## Default: random 10 character string
# mysqlRootPassword: testing

## Create a database user
##
# mysqlUser:
# mysqlPassword:

## Allow unauthenticated access, uncomment to enable
##
# mysqlAllowEmptyPassword: true

## Create a database
##
# mysqlDatabase:

## Specify an imagePullPolicy (Required)
## It's recommended to change this to 'Always' if the image tag is 'latest'
## ref: http://kubernetes.io/docs/user-guide/images/#updating-images
##
imagePullPolicy: IfNotPresent

livenessProbe:
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  successThreshold: 1
  failureThreshold: 3

readinessProbe:
  initialDelaySeconds: 5
  periodSeconds: 10
  timeoutSeconds: 1
  successThreshold: 1
  failureThreshold: 3

## Persist data to a persistent volume
persistence:
  enabled: true
  ## database data Persistent Volume Storage Class
  ## If defined, storageClassName: <storageClass>
  ## If set to "-", storageClassName: "", which disables dynamic provisioning
  ## If undefined (the default) or set to null, no storageClassName spec is
  ##   set, choosing the default provisioner.  (gp2 on AWS, standard on
  ##   GKE, AWS & OpenStack)
  ##
  # storageClass: "-"
  accessMode: ReadWriteOnce
  size: 8Gi

## Configure resource requests and limits
## ref: http://kubernetes.io/docs/user-guide/compute-resources/
##
resources:
  requests:
    memory: 256Mi
    cpu: 100m

# Custom mysql configuration files used to override default mysql settings
configurationFiles:
#  mysql.cnf: |-
#    [mysqld]
#    skip-name-resolve


## Configure the service
## ref: http://kubernetes.io/docs/user-guide/services/
service:
  ## Specify a service type
  ## ref: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services---service-types
  type: ClusterIP
  port: 3306
  # nodePort: 32000
```
### 修改配置并进行安装
```
# --set 设置多个键值对，以逗号为分隔符
helm install --set     mysqlRootPassword=test1234,mysqlDatabase=testdb,service.nodePort=32001,service.type=NodePort test-mysql azure/mysql
# -------------------结果-------------------------------
[root@VM-12-11-centos helm_charts]# helm install --set     mysqlRootPassword=test1234,mysqlDatabase=testdb,service.nodePort=32001,service.type=NodePort test-mysql azure/mysql
WARNING: Kubernetes configuration file is group-readable. This is insecure. Location: /etc/rancher/k3s/k3s.yaml
WARNING: Kubernetes configuration file is world-readable. This is insecure. Location: /etc/rancher/k3s/k3s.yaml
WARNING: This chart is deprecated
NAME: test-mysql
LAST DEPLOYED: Tue Jan 14 16:47:53 2025
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
MySQL can be accessed via port 3306 on the following DNS name from within your cluster:
test-mysql.default.svc.cluster.local

To get your root password run:

    MYSQL_ROOT_PASSWORD=$(kubectl get secret --namespace default test-mysql -o jsonpath="{.data.mysql-root-password}" | base64 --decode; echo)

To connect to your database:

1. Run an Ubuntu pod that you can use as a client:

    kubectl run -i --tty ubuntu --image=ubuntu:16.04 --restart=Never -- bash -il

2. Install the mysql client:

    $ apt-get update && apt-get install mysql-client -y

3. Connect using the mysql cli, then provide your password:
    $ mysql -h test-mysql -p

To connect to your database directly from outside the K8s cluster:
    MYSQL_HOST=$(kubectl get nodes --namespace default -o jsonpath='{.items[0].status.addresses[0].address}')
    MYSQL_PORT=$(kubectl get svc --namespace default test-mysql -o jsonpath='{.spec.ports[0].nodePort}')

    mysql -h ${MYSQL_HOST} -P${MYSQL_PORT} -u root -p${MYSQL_ROOT_PASSWORD}
```    
## 更新chart
```
helm update --set mysqlRootPassword=test1234,mysqlDatabase=testdb,service.nodePort=32001,service.type=NodePort test-mysql azure/mysql
```
## 查看chart修订历史
```
helm history test-mysql
```
## 回滚chart
```
helm rollback test-mysql 1
```
## 查看Helm帮助信息
```
helm get -h
```
## 问题列表：
1. K3s使用helm出现连接失败
```
# 问题异常
Error: Kubernetes cluster unreachable: Get "http://127.0.0.1:8080/version": read tcp 127.0.0.1:45436->127.0.0.1:8080: read: connection reset by peer - error from a previous attempt: read tcp 127.0.0.1:45428->127.0.0.1:8080: read: connection reset by peer
# 解决方案：临时
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
# 解决方案：永久（推荐，否则安装chart的时候部分功能没有权限）
vi /etc/profile
# 最后一行写入
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
# 激活
source /etc/profile
```
2. helm安装chart失败
```
# 问题
[root@VM-12-11-centos k8s_yaml]# helm install --set mysqlRootPassword=test1234,mysqlDatabase=testdb,service.nodePort=32001 test-mysql aliyuncs/mysql
WARNING: Kubernetes configuration file is group-readable. This is insecure. Location: /etc/rancher/k3s/k3s.yaml
WARNING: Kubernetes configuration file is world-readable. This is insecure. Location: /etc/rancher/k3s/k3s.yaml
Error: INSTALLATION FAILED: unable to build kubernetes objects from release manifest: resource mapping not found for name: "test-mysql-mysql" namespace: "" from "": no matches for kind "Deployment" in version "extensions/v1beta1"
# 方案
换一个仓库的chart
```