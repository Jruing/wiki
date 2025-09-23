## 1. ufw是什么

`ufw`（Uncomplicated Firewall）是 Ubuntu 及部分 Linux 发行版中提供的一款简化防火墙管理工具。
它基于 `iptables`/`nftables`，但封装了简洁易用的命令行接口，帮助用户快速完成防火墙规则配置（如端口开放、拒绝、限制访问等），而不必直接操作复杂的底层规则。

---

## 2. 原理是什么

ufw 的工作原理是：

* **底层依赖 iptables/nftables**：所有规则最终都会被转换为内核级的 `netfilter` 规则；
* **规则封装与抽象**：用户通过简化的命令（如 `ufw allow 22`），ufw 自动生成等价的 iptables/nftables 配置；
* **持久化与加载**：规则会写入 `/etc/ufw/` 目录下的配置文件，并在系统启动时自动加载；
* **流量处理流程**：

文字流程如下：

1. 网络数据包进入主机 → 进入 Linux 内核 netfilter 框架；
2. netfilter 根据 `iptables/nftables` 的规则进行检查；
3. ufw 提前写入的规则决定该数据包是否允许、拒绝、丢弃；
4. 结果反馈给内核网络栈 → 再交由应用层处理或直接丢弃。

---

## 3. 前提条件

使用 ufw 前需要：

* **操作系统**：基于 Debian/Ubuntu 的 Linux 系统（也可在其他系统中安装）；
* **组件**：

  * `iptables` 或 `nftables`（系统必须安装其中之一，通常默认自带）；
  * `ufw` 软件包（若未安装，可执行 `sudo apt install ufw` 安装）；
* **权限**：root 或具备 `sudo` 权限的用户；
* **环境**：建议在服务器启用 ufw 前确保存在 SSH 登录规则（避免误封）。

---

## 4. 可配置项有哪些

ufw 提供了以下常见可配置项：

* **基础控制**

  * `ufw enable` / `ufw disable`：启用/关闭防火墙
  * `ufw status`：查看规则状态

* **规则配置**

  * `ufw allow <port>`：允许指定端口
  * `ufw deny <port>`：拒绝指定端口
  * `ufw delete <rule>`：删除规则
  * `ufw allow from <IP>`：允许特定 IP 地址访问
  * `ufw allow from <IP> to any port <port>`：允许某 IP 访问指定端口
  * `ufw limit <port>`：限制端口连接速率（防止暴力破解，如 SSH）

* **默认策略**

  * `ufw default deny incoming`：默认拒绝所有进入流量
  * `ufw default allow outgoing`：默认允许所有外出流量

* **日志**

  * `ufw logging on|off|low|medium|high`：控制日志级别

---

## 5. 注意事项

* **避免锁死 SSH**：在远程服务器上启用 ufw 前，必须先执行 `ufw allow 22`。
* **规则顺序**：ufw 内部规则顺序会影响匹配结果，先匹配到的规则会优先生效。
* **持久化**：ufw 默认规则会写入配置文件，重启后仍然有效。
* **IPv6 支持**：若服务器启用了 IPv6，需要在 `/etc/default/ufw` 中启用 `IPV6=yes`。
* **日志文件**：相关日志记录在 `/var/log/ufw.log`。

---

## 6. 实践案例

### 案例1：常规服务器配置

```bash
# 安装并启用 ufw
sudo apt install ufw -y
sudo ufw enable

# 允许 SSH 远程登录
sudo ufw allow 22

# 允许 HTTP/HTTPS 服务
sudo ufw allow 80
sudo ufw allow 443

# 默认拒绝其他外部访问
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 查看规则状态
sudo ufw status verbose
```

### 案例2：只允许某 IP 访问数据库

```bash
# 假设数据库端口为 3306，只允许 192.168.1.100 访问
sudo ufw allow from 192.168.1.100 to any port 3306
```

### 案例3：限制 SSH 暴力破解

```bash
# 使用 limit 限制 SSH 登录失败次数
sudo ufw limit ssh
```