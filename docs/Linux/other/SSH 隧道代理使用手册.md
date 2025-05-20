# 🔐 SSH 隧道代理使用手册

> SSH 不仅是一个安全登录工具，还可以通过其隧道功能实现端口转发，从而绕过防火墙限制、加密网络通信等。以下是 SSH 隧道的基本概念和常见用法。

---

## 一、SSH 隧道类型概述

| 类型 | 参数格式                               | 中文名称                           | 功能描述                                                     |
| ---- | -------------------------------------- | ---------------------------------- | ------------------------------------------------------------ |
| `-L` | `-L [bind_address:]port:host:hostport` | 本地端口转发（Local Forwarding）   | 将本地端口请求通过 SSH 转发到远程服务器的目标主机和端口      |
| `-R` | `-R [bind_address:]port:host:hostport` | 远程端口转发（Remote Forwarding）  | 将远程服务器上的某个端口请求通过 SSH 转发到本地机器的目标主机和端口 |
| `-D` | `-D [bind_address:]port`               | 动态端口转发（Dynamic Forwarding） | 建立一个 SOCKS 代理服务器，可用于浏览器或支持 SOCKS 的程序   |

---

## 二、详细说明与示例

### 1. 本地端口转发（Local Forwarding）

#### 📌 概念：
将本机的一个端口监听起来，并将所有连接请求通过 SSH 隧道转发到远程服务器上指定的主机和端口。

#### 🔧 语法：
```bash
ssh -L [本地绑定地址:]本地端口:目标主机:目标端口 用户名@SSH服务器
```

#### 🧩 示例：

你希望访问公司内网中的一台数据库服务器 `dbserver`（IP：192.168.1.100），但只能通过跳板机 `jumpbox` 访问。

```bash
ssh -L 3306:192.168.1.100:3306 user@jumpbox
```

这样你就可以在本地通过 `localhost:3306` 访问远程数据库了。

#### ✅ 参数解释：

- `3306`: 本地监听的端口
- `192.168.1.100:3306`: 内网目标主机和端口
- `user@jumpbox`: SSH 登录跳板机

---

### 2. 远程端口转发（Remote Forwarding）

#### 📌 概念：
将远程服务器上的某个端口监听起来，并将所有连接请求通过 SSH 反向转发到本地机器的目标主机和端口。

#### 🔧 语法：
```bash
ssh -R [远程绑定地址:]远程端口:目标主机:目标端口 用户名@SSH服务器
```

#### 🧩 示例：

你在家里有一台 Web 服务运行在 `localhost:8080`，你想让公网上的某台 VPS 能访问它。

```bash
ssh -R 80:localhost:8080 user@vps.example.com
```

这样公网用户访问 `vps.example.com:80` 就会被转发到你家里的 `localhost:8080`。

#### ✅ 参数解释：

- `80`: VPS 上监听的端口
- `localhost:8080`: 本地目标主机和端口
- `user@vps.example.com`: SSH 登录 VPS 地址

> ⚠️ 注意：需要在 `/etc/ssh/sshd_config` 中设置 `GatewayPorts yes` 才能允许外部访问。

---

### 3. 动态端口转发（Dynamic Forwarding）

#### 📌 概念：
建立一个本地 SOCKS 代理服务，所有通过该代理的流量都会通过 SSH 加密传输，常用于翻墙或安全浏览网页。

#### 🔧 语法：
```bash
ssh -D [绑定地址:]本地SOCKS端口 用户名@SSH服务器
```

#### 🧩 示例：

你想通过远程服务器建立一个本地代理，访问互联网时走这个代理。

```bash
ssh -D 1080 user@remote-server
```

然后配置浏览器使用 SOCKS5 代理：
- 协议：SOCKS5
- 地址：`127.0.0.1`
- 端口：`1080`

#### ✅ 参数解释：

- `1080`: 本地监听的 SOCKS5 代理端口
- `user@remote-server`: SSH 登录服务器

---

## 三、常用参数说明

| 参数 | 含义                                                     |
| ---- | -------------------------------------------------------- |
| `-f` | 在后台运行 SSH                                           |
| `-N` | 不执行远程命令，只用于建立隧道                           |
| `-g` | 允许远程主机连接本地转发端口（需配合 GatewayPorts 使用） |
| `-C` | 启用压缩                                                 |
| `-q` | 静默模式                                                 |
| `-T` | 禁用伪终端分配（适用于仅做转发的情况）                   |

#### 示例组合：

```bash
ssh -f -N -T -g -R 8080:localhost:80 user@vps.example.com
```

这条命令会在后台运行，不分配终端，启用远程转发，把 VPS 上的 8080 端口映射到本地的 80 端口。

---

## 四、应用场景总结

| 场景                                | 推荐方式                      |
| ----------------------------------- | ----------------------------- |
| 本地访问远程内网服务（如数据库）    | 本地转发 `-L`                 |
| 外部访问本地服务（如 Web 本地开发） | 远程转发 `-R`                 |
| 安全浏览网页 / 翻墙                 | 动态转发 `-D`                 |
| 自动保持隧道连接                    | 结合 `autossh` 工具           |
| 多人共享本地服务                    | 远程转发 + `GatewayPorts yes` |

---

## 五、进阶技巧

### 1. 使用 `autossh` 自动重连

```bash
autossh -M 20000 -f -N -R 80:localhost:8080 user@vps.example.com
```

- `-M 20000`: autossh 用来检测连接状态的监控端口

### 2. 配置文件自动建立隧道

编辑 `~/.ssh/config` 文件：

```bash
Host tunnel
    HostName vps.example.com
    User user
    RemoteForward 80 localhost:8080
    GatewayPorts yes
    ExitOnForwardFailure yes
```

然后只需：
```bash
ssh -N tunnel
```

即可自动建立远程转发。

---

## 六、常见问题 FAQ

### Q1: 出现 `bind: Cannot assign requested address` 错误？
A: 检查是否指定了错误的绑定地址，例如 `0.0.0.0` 需要权限或已占用。

### Q2: 为什么远程转发别人访问不了？
A: 默认只允许本地访问，需要添加 `GatewayPorts yes` 到 `/etc/ssh/sshd_config` 并重启 sshd。

### Q3: 如何查看当前监听的端口？
A: 使用：
```bash
netstat -tuln
```
或者：
```bash
ss -tuln
```

---

## 七、附录：完整命令示例表

| 类型     | 示例命令                                         |
| -------- | ------------------------------------------------ |
| 本地转发 | `ssh -L 3306:mysql.int:3306 user@gateway`        |
| 远程转发 | `ssh -R 8080:localhost:3000 user@vps`            |
| 动态转发 | `ssh -D 1080 user@proxy`                         |
| 后台运行 | `ssh -f -N -L 8080:local:80 user@server`         |
| 自动重连 | `autossh -M 20000 -f -N -R 80:local:80 user@vps` |

