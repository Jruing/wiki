
---

# 📘 iptables 学习手册（完整版）

## 目录

1. [什么是 iptables？](#1-什么是-iptables)
2. [iptables 的结构与原理](#2-iptables-的结构与原理)
3. [基本命令语法](#3-基本命令语法)
4. [常用参数说明](#4-常用参数说明)
5. [链（Chain）与表（Table）](#5-链chain-与表table)
6. [常见操作：添加、删除、查看规则](#6-常见操作添加删除查看规则)
7. [保存与恢复规则](#7-保存与恢复规则)
8. [常用防火墙策略示例](#8-常用防火墙策略示例)
9. [端口开放与限制访问](#9-端口开放与限制访问)
10. [IP 限制与黑白名单](#10-ip-限制与黑白名单)
11. [状态匹配（连接追踪）](#11-状态匹配连接追踪)
12. [日志记录](#12-日志记录)
13. [NAT 配置](#13-nat-配置)
14. [高级用法：自定义链](#14-高级用法自定义链)
15. [实战案例](#15-实战案例)
16. [常见问题解答](#16-常见问题解答)

---

## 1. 什么是 iptables？

`iptables` 是 Linux 内核中用于管理网络数据包过滤的工具，它允许你定义规则来控制进出系统的网络流量。它是 Linux 防火墙的核心组件之一。

---

## 2. iptables 的结构与原理

iptables 通过 **表（tables）** 和 **链（chains）** 来组织规则：

- **表（Tables）**：不同的表处理不同类型的任务
  - `filter`：默认表，用于过滤流量（如放行/拒绝）
  - `nat`：用于地址转换（如 SNAT/DNAT）
  - `mangle`：修改数据包头部信息
  - `raw`：用于配置连接追踪
- **链（Chains）**：每个表中有多个链，对应不同阶段的数据包处理
  - `INPUT`：进入本机的数据包
  - `OUTPUT`：本机发出的数据包
  - `FORWARD`：转发到其他主机的数据包
  - `PREROUTING`：路由前修改目标地址（NAT 使用）
  - `POSTROUTING`：路由后修改源地址（NAT 使用）

---

## 3. 基本命令语法

```bash
iptables [-t 表名] 命令 链名 [规则匹配条件] [-j 动作]
```

---

## 4. 常用参数说明

| 参数 | 含义 |
|------|------|
| `-A` | Append，在链末尾追加一条规则 |
| `-I` | Insert，在指定位置插入规则 |
| `-D` | Delete，删除某条规则 |
| `-L` | List，列出规则 |
| `-F` | Flush，清空所有规则 |
| `-Z` | Zero，清零计数器 |
| `-P` | Policy，设置链的默认策略 |
| `-v` | 显示详细信息 |
| `-n` | 不进行 DNS 解析，显示 IP 和端口号 |

---

## 5. 链（Chain）与表（Table）

### 示例：

```bash
# 查看 filter 表中的 INPUT 链规则
iptables -t filter -L INPUT -n -v

# 查看 nat 表的所有链规则
iptables -t nat -L -n -v
```

---

## 6. 常见操作：添加、删除、查看规则

### 添加规则（允许 SSH）：

```bash
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

### 删除规则（按编号删除）：

```bash
iptables -L INPUT --line-numbers  # 查看规则编号
iptables -D INPUT 3               # 删除第 3 条规则
```

### 清空规则：

```bash
iptables -F
```

### 设置默认策略（禁止所有入站）：

```bash
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
```

---

## 7. 保存与恢复规则

### CentOS / RHEL：

```bash
service iptables save
```

或手动保存：

```bash
iptables-save > /etc/iptables/rules.v4
```

恢复规则：

```bash
iptables-restore < /etc/iptables/rules.v4
```

### Ubuntu / Debian：

安装 `iptables-persistent` 包：

```bash
apt install iptables-persistent
```

保存规则：

```bash
netfilter-persistent save
```

---

## 8. 常用防火墙策略示例

### 最小化防火墙策略（仅允许本地环回 + 已建立连接）：

```bash
iptables -F
iptables -X
iptables -t nat -F
iptables -t mangle -F
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
```

---

## 9. 端口开放与限制访问

### 允许 HTTP 和 HTTPS：

```bash
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

### 拒绝某个端口：

```bash
iptables -A INPUT -p tcp --dport 25 -j DROP
```

---

## 10. IP 限制与黑白名单

### 屏蔽单个 IP：

```bash
iptables -A INPUT -s 192.168.1.100 -j DROP
```

### 允许特定 IP 访问 SSH：

```bash
iptables -A INPUT -p tcp --dport 22 -s 192.168.1.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j DROP
```

### 白名单模式（只允许白名单 IP）：

```bash
iptables -A INPUT -s 192.168.1.100 -j ACCEPT
iptables -A INPUT -s 10.0.0.0/24 -j ACCEPT
iptables -A INPUT -j DROP
```

---

## 11. 状态匹配（连接追踪）

```bash
# 允许已建立连接和相关流量
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
```

---

## 12. 日志记录

```bash
# 记录被拒绝的数据包
iptables -A INPUT -j LOG --log-prefix "IPTABLES-DROP: "
```

> 日志会写入 `/var/log/kern.log` 或 `/var/log/messages`，取决于系统配置。

---

## 13. NAT 配置

### SNAT（源地址转换）：

```bash
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

### DNAT（目标地址转换）：

```bash
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.10:8080
```

---

## 14. 高级用法：自定义链

```bash
# 创建自定义链
iptables -N BLACKLIST

# 添加规则到自定义链
iptables -A BLACKLIST -s 192.168.1.100 -j DROP
iptables -A BLACKLIST -s 10.0.0.0/24 -j DROP

# 在主链中引用自定义链
iptables -A INPUT -j BLACKLIST
```

---

## 15. 实战案例

### ✅ 案例一：Web 服务器防火墙

```bash
# 默认策略
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# 允许本地环回
iptables -A INPUT -i lo -j ACCEPT

# 已建立连接允许
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# 允许 SSH、HTTP、HTTPS
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# 屏蔽黑名单 IP
iptables -A INPUT -s 192.168.1.100 -j DROP
```

---

### ✅ 案例二：NAT 路由器配置

```bash
# 开启内核转发
echo 1 > /proc/sys/net/ipv4/ip_forward

# 配置 NAT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# 允许内部网络访问
iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
```

---

## 16. 常见问题解答

### Q1：为什么我设置了规则但无法访问服务？

- 检查默认策略是否为 `DROP`
- 规则顺序很重要，越具体的规则应放在前面
- 是否清除了旧规则？
- 是否开启了内核转发（NAT 场景）？

### Q2：如何查看规则编号？

```bash
iptables -L INPUT --line-numbers
```

### Q3：如何阻止 ICMP（Ping）请求？

```bash
iptables -A INPUT -p icmp --icmp-type echo-request -j DROP
```

---

## 📚 推荐资源

- 官方文档：[https://www.netfilter.org/documentation/](https://www.netfilter.org/documentation/)
- `man iptables`：Linux 下直接查看帮助文档
- `iptables-extensions`：扩展模块使用指南
- 社区论坛：[https://forum.netfilter.org/](https://forum.netfilter.org/)

---