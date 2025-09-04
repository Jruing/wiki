## 创建宿主机目录与配置文件
```
# 1. 创建目录（数据目录、配置目录）
mkdir -p /opt/redis/{data,conf}

# 2. 赋予权限（避免容器内无法写入数据）
chown -R 1000:1000 /opt/redis
chmod -R 755 /opt/redis
```
## 配置文件
```
# ====================== 基础配置 ======================
# 绑定地址（Docker 内可绑定 0.0.0.0，允许外部访问）
bind 0.0.0.0
# 端口（默认 6379）
port 6379
# 保护模式（关闭，允许非本地访问，需配合密码）
protected-mode no
# 密码（必填，避免未授权访问）
requirepass YourStrongPassword123!

# ====================== 持久化配置（核心） ======================
# 1. AOF 配置（开启+每秒刷盘）
# 开启 AOF
appendonly yes 
# AOF 文件名
appendfilename "appendonly.aof"  
# 刷盘策略：每秒同步1次（平衡安全与性能）
appendfsync everysec             
 # AOF 重写时暂停刷盘，避免性能波动
no-appendfsync-on-rewrite yes   

# 2. RDB 配置（定期快照，作为备份）
 # 3600秒内有1次写操作，生成快照
save 3600 1   
 # 300秒内有100次写操作，生成快照
save 300 100  
# 60秒内有10000次写操作，生成快照
save 60 10000  
 # RDB 文件名
dbfilename dump.rdb             
 # 开启 RDB 压缩（节省空间）
rdbcompression yes              

# ====================== 数据目录配置（与Docker挂载对应） ======================
# Redis 数据目录（容器内路径，需挂载到宿主机）
dir /data  

# ====================== 其他优化配置 ======================
# 最大内存限制（避免 Redis 耗尽宿主机内存）
# 根据宿主机内存调整，如 4GB
maxmemory 4g 
# 内存满时的淘汰策略（优先删除过期键）
maxmemory-policy allkeys-lru
# 容器内后台运行（Docker 需前台运行，故关闭）
daemonize no
# 日志级别（生产环境用 notice）
loglevel notice
# 日志文件（输出到容器stdout，便于 docker logs 查看）
logfile ""
```

## 启动容器
```
docker run -d \
  --name redis-persist \
  --restart always \  # 容器退出时自动重启（避免意外崩溃）
  -p 6379:6379 \      # 端口映射（宿主机端口:容器端口）
  # 挂载数据卷：宿主机目录 -> 容器目录
  -v /opt/redis/conf/redis.conf:/etc/redis/redis.conf \  # 配置文件挂载
  -v /opt/redis/data:/data \  # 数据目录挂载（含 RDB/AOF 文件）
  # 启动命令：指定加载自定义配置
  redis:7.2-alpine redis-server /etc/redis/redis.conf
```
