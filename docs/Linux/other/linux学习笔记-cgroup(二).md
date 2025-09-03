cgroups (Control Groups) 是 Linux 内核功能，用于限制、记录和隔离进程组的资源使用（CPU、内存、磁盘I/O、网络等）。cgroup v2 是 cgroups 的第二代实现，提供了更统一和一致的接口。

## 一、cgroup v2 核心概念

1. **层级结构(Hierarchy)**：v2 采用单一层级结构，所有控制器挂载在统一视图下
2. **控制器(Controllers)**：资源控制模块（如 cpu、memory、io 等）
3. **cgroup 路径**：每个 cgroup 在虚拟文件系统中有唯一路径
4. **进程归属**：进程可属于任意 cgroup，受该 cgroup 资源限制

## 二、基本操作步骤

### 1. 挂载 cgroup v2 文件系统

```bash
# 检查当前系统是否已启用 cgroup v2
mount | grep cgroup

# 若未启用，在 /etc/fstab 中添加
cgroup2 /sys/fs/cgroup cgroup2 rw,relatime,nsdelegate 0 0

# 临时挂载
mount -t cgroup2 cgroup2 /sys/fs/cgroup
```

### 2. 创建和删除 cgroup

```bash
# 进入 cgroup 根目录
cd /sys/fs/cgroup

# 创建新 cgroup（自动创建子目录）
mkdir myapp_group

# 删除 cgroup
rmdir myapp_group
```

### 3. 启用资源控制器

```bash
# 查看当前可用的控制器
cat cgroup.controllers

# 启用控制器（如 memory 和 cpu）
echo '+memory +cpu' > cgroup.subtree_control

# 验证已启用控制器
cat cgroup.subtree_control
```

## 三、资源控制示例

### 1. CPU 限制

**示例：限制进程最多使用 1 个 CPU 核心（100ms/100ms）**

```bash
# 创建 cgroup
mkdir cpu_limit_group

# 启用 CPU 控制器
echo '+cpu' > cgroup.subtree_control

# 设置 CPU 配额（周期 100ms，配额 100ms）
echo '100000' > cpu_limit_group/cpu.max

# 将进程 PID 添加到 cgroup
echo 1234 > cpu_limit_group/cgroup.procs
```

### 2. 内存限制

**示例：限制内存使用不超过 1GB**

```bash
# 创建 cgroup
mkdir mem_limit_group

# 启用 memory 控制器
echo '+memory' > cgroup.subtree_control

# 设置内存硬限制（1GB）
echo '1G' > mem_limit_group/memory.max

# 设置 OOM 优先级（可选）
echo '100' > mem_limit_group/memory.oom.group

# 添加进程
echo 5678 > mem_limit_group/cgroup.procs
```

### 3. 磁盘 I/O 限制

**示例：限制磁盘读写带宽**

```bash
# 创建 cgroup
mkdir io_limit_group

# 启用 io 控制器
echo '+io' > cgroup.subtree_control

# 查找磁盘设备号（如 /dev/sda）
lsblk -d -o NAME,MAJ:MIN

# 设置读带宽限制（10MB/s）
echo '254:0 rbps=10485760' > io_limit_group/io.max

# 设置写 IOPS 限制（1000 iops）
echo '254:0 wiops=1000' > io_limit_group/io.max
```

### 4. 混合资源限制

**示例：为 Web 服务设置综合资源限制**

```bash
# 创建 cgroup
mkdir web_service

# 启用所有可用控制器
echo '+cpu +memory +io +pids' > cgroup.subtree_control

# CPU 限制（50% 单核）
echo '50000 100000' > web_service/cpu.max

# 内存限制（2GB）
echo '2G' > web_service/memory.max

# 进程数限制（100 进程）
echo '100' > web_service/pids.max

# 启动服务并加入 cgroup
systemd-run --scope -p MemoryMax=2G -p CPUQuota=50% /opt/webapp/start.sh
```

## 四、高级功能示例

### 1. 资源统计监控

```bash
# 查看内存使用统计
cat memory.current
cat memory.stat

# 查看 CPU 使用统计
cat cpu.stat

# 查看 IO 统计
cat io.stat
```

### 2. OOM 控制

```bash
# 禁用某 cgroup 的 OOM 杀手（当内存超限时直接报错而非 kill 进程）
echo '1' > memory.oom.group

# 查看 OOM 事件
cat memory.oom.group
```

### 3. 嵌套 cgroup 结构

```bash
# 创建父 cgroup
mkdir parent_group
echo '+cpu +memory' > parent_group/cgroup.subtree_control

# 创建子 cgroup
mkdir parent_group/child1
echo '50000 100000' > parent_group/child1/cpu.max

mkdir parent_group/child2
echo '25000 100000' > parent_group/child2/cpu.max

# 父 cgroup 设置总限制
echo '75000 100000' > parent_group/cpu.max
```

## 五、Docker 中的 cgroup v2

Docker 从 20.10 版本开始支持 cgroup v2。使用示例如：

```bash
# 运行容器时指定资源限制（自动创建 cgroup）
docker run -d \
  --cpus=1.5 \
  --memory=512m \
  --blkio-weight=300 \
  --name mycontainer \
  nginx:alpine

# 查看容器对应的 cgroup
systemd-cgls | grep docker
```

## 六、注意事项

1. 修改 `cgroup.subtree_control` 会影响所有子 cgroup
2. 资源限制值必须满足父 cgroup 的约束
3. 某些控制器（如 `cpuset`）需要额外配置
4. 系统重启后 cgroup 配置不会持久化，需通过 systemd 或脚本实现持久化
5. 使用 `nsdelegate` 挂载选项时，命名空间内的 cgroup 操作会被委派给容器

通过以上方法，可以有效地利用 cgroup v2 对系统资源进行精细化管理，确保关键应用的服务质量（QoS），同时防止资源滥用导致的系统不稳定。