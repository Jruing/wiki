> 安装高版本Redis需要先安装Python3.x

## 下载

https://download.redis.io/redis-stable.tar.gz

## 部署

1. 上传解压

   ```
   tar -zxvf  redis-stable.tar.gz
   ```

2. 编译安装

   ```
   cd redis-stable
   # 如果make出现异常，可以尝试make MALLOC=libc
   make 
   # 将redis安装到/usr/local/redis-stable目录下
   make PREFIX=/usr/local/redis-stable install
   ```

3. 创建6个节点的目录

   ```
   # 创建日志目录
   mkdir -p /usr/local/redis-cluster/{6379,6380,6381,6382,6383,6384}/log
   # 创建配置文件目录
   mkdir -p /usr/local/redis-cluster/{6379,6380,6381,6382,6383,6384}/config
   ```

4. 写入配置文件(写入配置的时候请务必去掉注释)

   ```
   # 6379节点配置文件
   cat << EOF > /usr/local/redis-cluster/6379/config/redis.conf
   protected-mode no
   bind 0.0.0.0
   port 6379 # 服务监听端口
   daemonize yes # 后台启动
   pidfile /usr/local/redis-cluster/6379/redis_6379.pid
   masterauth test-cluster # 启动 redis 密码验证，主要是针对 master 对应的 slave 节点设置的，在 slave 节点数据同步的时候用到
   requirepass test-cluster # redis密码，#启动 redis 密码验证，一定要 requirepass 和 masterauth 同时设置。对登录权限做限制，redis每个节点的requirepass可以是独立、不同的，但建议和 masterauth 设置成一样
   appendonly yes # 开启持久化
   dir /usr/local/redis-cluster/6379/ # AOF文件存放目录
   appendfilename "appendonly.aof" #AOF文件名称（默认）
   cluster-enabled yes # 启用集群
   cluster-config-file "nodes.conf" # 关联集群的配置文件
   cluster-node-timeout 5000 # 集群超时时间
   cluster-require-full-coverage no # 只要有结点宕机导致 16384 个槽没全被覆盖，整个集群就全部停止服务，所以一定要改为 no
   EOF
   
   # 6380节点配置文件
   cat << EOF > /usr/local/redis-cluster/6380/config/redis.conf
   protected-mode no
   bind 0.0.0.0
   port 6380
   daemonize yes
   pidfile /usr/local/redis-cluster/6380/redis_6380.pid
   masterauth test-cluster
   requirepass test-cluster 
   appendonly yes
   dir /usr/local/redis-cluster/6380/
   appendfilename "appendonly.aof" 
   cluster-enabled yes
   cluster-config-file "nodes.conf"
   cluster-node-timeout 5000
   cluster-require-full-coverage no
   EOF
   
   # 6381,6382,6383,6384配置文件参考上面的
   
   ```

5. 分别启动redis

   ```
   redis-server /usr/local/redis-cluster/6379/config/redis.conf
   redis-server /usr/local/redis-cluster/6380/config/redis.conf
   redis-server /usr/local/redis-cluster/6381/config/redis.conf
   redis-server /usr/local/redis-cluster/6382/config/redis.conf
   redis-server /usr/local/redis-cluster/6383/config/redis.conf
   redis-server /usr/local/redis-cluster/6387/config/redis.conf
   ```

6. 创建集群

   ```
   redis-cli -a "test-cluster" --cluster create 192.168.137.10:6379 192.168.137.10:6380 192.168.137.10:6381 192.168.137.10:6382 192.168.137.10:6383 192.168.137.10:6384 --cluster-replicas 1
   ```

7. 验证集群

   ```
   redis-cli -h 192.168.137.10 -c -p 6380 -a "test-cluster"
   ```

8. 集群查看相关命令

   ```
   1.集群状态
   redis-cli -h ip -p 6401 -a password cluster info
   2.集群节点信息
   redis-cli -h ip -p 6401 -a password cluster nodes
   3.节点内存、cpu、key数量等信息（每个节点都需查看）
   redis-cli -h ip -p 6401 -a password info
   ```

   
