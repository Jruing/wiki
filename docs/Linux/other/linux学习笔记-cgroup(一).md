#  Linux学习笔记-cgroup(一)

## 概念

> **cgroup（控制组）** 是 Linux 内核提供的一种资源管理机制，它能够将一组进程组织起来，并对它们的资源使用进行限制、监控和隔离。
>
> cgroup分为2个版本：
>
> v1:最初设计，资源控制通过多个独立的子系统（controller）分别管理
>
> v2:重构设计，统一管理接口，增强一致性和简化配置，现代系统推荐使用。

## 主要用途

- Linux 进程默认共享系统资源，没有限制，cgroup则允许管理员在系统上对任何进程的资源利用进行限制
- 容器技术（如 Docker、Podman、Kubernetes）底层大量依赖 cgroup 来实现资源隔离和限制。

## 核心功能

- **资源限制（Resource Limiting）**
   限制某组进程能使用的 CPU、内存、磁盘 IO、网络带宽等资源。

- **资源计量（Resource Accounting）**
   统计进程组资源使用情况，方便监控和分析。

- **资源控制（Resource Control）**
   可以根据策略动态调整资源分配。

- **进程组织（Process Grouping）**
   把多个进程归为一组，方便统一管理。

## 组成部分

1. **控制组层级（Hierarchy）**
    类似目录树结构，一个层级可以挂载多个控制器。
2. **控制器（Controller）**
   负责具体资源的管理，如下：
   - `cpu`：CPU 使用限制与调度
   - `memory`：内存使用限制
   - `blkio`：块设备 IO 限制
   - `cpuset`：绑定 CPU 和内存节点
   - `net_cls`、`net_prio`：网络相关
3. **任务（Tasks）**
    进程 PID，可以被加入到某个 cgroup 中。
4. **控制文件（Control files）**
    每个 cgroup 目录下有很多文件，用户通过读写这些文件来配置和监控资源。

## cgroup相关文件目录结构图

```
/sys/fs/cgroup（cgroup根目录，所有子系统的起点）
├─ 核心控制文件（跨子系统的通用管理文件，负责进程组的基础管理）
│  ├─ cgroup.procs          # 记录当前cgroup中的进程PID（线程组ID），写入PID可将进程加入该组
│  ├─ tasks                 # 记录当前cgroup中的线程TID（比cgroup.procs粒度更细，含所有线程）
│  ├─ cgroup.subtree_control # 控制子cgroup的资源管控权限（如"+cpu +memory"允许子组限制CPU和内存）
│  └─ cgroup.controllers    # 列出当前cgroup支持的资源控制器（子系统），如"cpu memory blkio"
│
├─ cpu,cpuacct（CPU资源控制与统计子系统）
│  ├─ cpu.cfs_period_us     # CPU调度周期（默认100000微秒=0.1秒），用于计算CPU时间分配比例
│  ├─ cpu.cfs_quota_us      # 周期内可使用的CPU时间（如50000表示占1核的50%，-1表示无限制）
│  ├─ cpu.shares            # CPU权重（相对值，默认1024，值越高竞争CPU时优先级越高）
│  ├─ cpuacct.usage         # 累计使用的CPU总时间（纳秒），用于统计资源消耗
│  └─ cpuacct.usage_percpu  # 按每个CPU核心统计的累计使用时间，支持多核心场景监控
│
├─ memory（内存资源控制与监控子系统）
│  ├─ memory.limit_in_bytes # 最大内存使用限制（字节，如104857600=100MB，超限时触发OOM）
│  ├─ memory.soft_limit_in_bytes # 内存软限制（系统内存充足时可超过，紧张时优先回收）
│  ├─ memory.usage_in_bytes # 当前内存使用量（含缓存、匿名页等，实时反映资源占用）
│  ├─ memory.stat           # 详细内存统计（如total_rss=物理内存使用，swap=交换分区使用）
│  └─ memory.oom_control    # OOM控制开关（oom_kill_disable=1禁用自动杀死进程，需手动处理）
│
├─ blkio（块设备IO资源控制子系统，管理磁盘读写）
│  ├─ blkio.throttle.read_bps_device  # 限制设备读速度（格式"主设备号:次设备号 速率"，如"8:0 104857600"=100MB/s）
│  ├─ blkio.throttle.write_bps_device # 限制设备写速度（同上，控制写入磁盘的速率）
│  ├─ blkio.weight          # IO权重（相对值，默认100，值越高竞争IO资源时优先级越高）
│  └─ blkio.io_service_bytes # 按设备统计的读写总字节数，用于监控IO消耗
│
├─ pids（进程数量限制子系统，防止进程无限创建）
│  ├─ pids.max              # 最大允许的进程/线程总数（如100表示最多创建100个进程）
│  └─ pids.current          # 当前cgroup中的进程总数，实时反映进程数量变化
│
└─ net_cls,net_prio（网络资源标记与优先级子系统）
   ├─ net_cls.classid       # 为进程网络包添加类别标记（配合tc工具实现网络限流）
   └─ net_prio.prio         # 网络优先级（0-7，值越低优先级越高，影响数据包发送顺序）
```

## 工作流程(内存限制示例)

![Cgroup 内存限制流程及绘图](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/Cgroup%20%E5%86%85%E5%AD%98%E9%99%90%E5%88%B6%E6%B5%81%E7%A8%8B%E5%8F%8A%E7%BB%98%E5%9B%BE.png)

## 应用场景

- **容器资源隔离**：Docker/Podman 用 cgroup 限制容器资源使用。

- **服务器资源隔离**：在多用户或多服务共享的服务器上，cgroup 可隔离不同服务的资源，防止某一服务异常占用资源导致其他服务崩溃

- **IO 资源控制**：除 CPU 和内存外，cgroup 的`blkio`子系统可限制进程的磁盘 IO 速度，避免某一进程的大量 IO 操作拖慢整个存储系统。

-  **防止进程 OOM 与系统稳定性**：对于可能因内存泄漏而无限占用内存的进程，cgroup 可设置内存上限，当达到上限时触发 OOM 杀死进程，避免影响整个系统。

