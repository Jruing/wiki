# ServerLess学习笔记-搭建FnProject

## 介绍

> 官方文档：https://fnproject.io/tutorials/
>
> Fn 是一个事件驱动的开源功能即服务 FaaS计算平台，您可以在任何地方运行,它的一些主要特点
>
> - 开源
> - 原生 Docker：使用任何 Docker 容器作为你的函数
> - 支持所有语言
> - 随处运行
>     - 公有云、私有云和混合云
>     - 导入 Lambda 函数并在任何地方运行它们
> - 易于开发人员使用
> - 易于操作员管理
> - 简单而强大的可扩展性

## 前提条件

> - Docker 17.10.0-ce 或更高版本
> - 注册DockerHub账号（非必须，如果使用本地模式则不需要，如果需要将服务推动到仓库则需要）

## Linux安装

### 方式1 (通过脚本安装)

```shell
curl -LSs https://raw.githubusercontent.com/fnproject/cli/master/install | sh
```

### 方式2 (二进制安装)

```shell
下载
wget -o fn https://github.com/fnproject/fn/releases/download/0.3.25/fn_linux
# 赋予可执行权限
chmod +x fn
```

## 启动服务

> 启动命令：`./fn start`
>
> 注意：默认使用8080端口及2375端口，若想修改为其他的端口需要执行`fn start -p 8081`及配置环境变量 `export FN_API_URL=http://127.0.0.1:8081`

```
[root@localhost-centos serverless]# ./fn start
2023/10/19 18:02:02 ¡¡¡ 'fn start' should NOT be used for PRODUCTION !!! see https://github.com/fnproject/fn-helm/
time="2023-10-19T10:02:02Z" level=info msg="Setting log level to" fields.level=info
time="2023-10-19T10:02:02Z" level=info msg="Registering data store provider 'sql'"
time="2023-10-19T10:02:02Z" level=info msg="Connecting to DB" url="sqlite3:///app/data/fn.db"
time="2023-10-19T10:02:02Z" level=info msg="datastore dialed" datastore=sqlite3 max_idle_connections=256 url="sqlite3:///app/data/fn.db"
time="2023-10-19T10:02:02Z" level=info msg="agent starting cfg={MinDockerVersion:17.10.0-ce ContainerLabelTag: DockerNetworks: DockerLoadFile: DisableUnprivilegedContainers:false FreezeIdle:50ms HotPoll:200ms HotLauncherTimeout:1h0m0s HotPullTimeout:10m0s HotStartTimeout:5s DetachedHeadRoom:6m0s MaxResponseSize:0 MaxHdrResponseSize:0 MaxLogSize:1048576 MaxTotalCPU:0 MaxTotalMemory:0 MaxFsSize:0 MaxPIDs:50 MaxOpenFiles:0xc420486518 MaxLockedMemory:0xc420486530 MaxPendingSignals:0xc420486538 MaxMessageQueue:0xc420486540 PreForkPoolSize:0 PreForkImage:busybox PreForkCmd:tail -f /dev/null PreForkUseOnce:0 PreForkNetworks: EnableNBResourceTracker:false MaxTmpFsInodes:0 DisableReadOnlyRootFs:false DisableDebugUserLogs:false IOFSEnableTmpfs:false EnableFDKDebugInfo:false IOFSAgentPath:/iofs IOFSMountRoot:/root/.fn/iofs IOFSOpts: ImageCleanMaxSize:0 ImageCleanExemptTags: ImageEnableVolume:false}"
time="2023-10-19T10:02:02Z" level=info msg="no docker auths from config files found (this is fine)" error="open /root/.dockercfg: no such file or directory"
time="2023-10-19T10:02:02Z" level=info msg="available memory" cgroup_limit=9223372036854771712 head_room=295451443 total_memory=2954514432
time="2023-10-19T10:02:02Z" level=info msg="ram reservations" avail_memory=2659062989
time="2023-10-19T10:02:02Z" level=info msg="available cpu" avail_cpu=4000 total_cpu=4000
time="2023-10-19T10:02:02Z" level=info msg="cpu reservations" cpu=4000
time="2023-10-19T10:02:02Z" level=info msg="\n        ______\n       / ____/___\n      / /_  / __ \\\n     / __/ / / / /\n    /_/   /_/ /_/\n"
time="2023-10-19T10:02:02Z" level=info msg="Fn serving on `:8080`" type=full version=0.3.750

```

