> rsync 是一个强大的文件同步工具，用于在本地或远程系统之间高效地复制和同步文件。它通过**增量传输**算法（只传输文件的不同部分）大幅减少网络传输量，并支持多种高级功能（如压缩、加密、权限保留等）。

### **一、基本原理**

- **增量传输**：仅同步源和目标之间有差异的部分，而非整个文件。

- **校验机制**：通过文件大小和时间戳快速判断差异，必要时使用校验和（如 MD5）精确比对。

- **压缩传输**：在传输过程中对数据进行压缩，减少网络流量。

### **二、安装**

#### **Linux**

```
# Debian/Ubuntu
sudo apt-get install rsync

# CentOS/RHEL
sudo yum install rsync
```

#### **macOS**

```
# 默认已安装，或通过 Homebrew 更新
brew install rsync
```

#### **Windows**

- 安装 **Cygwin** 或 **MinGW** 环境，包含 rsync。

- 使用 **Git Bash**（自带 rsync）。

- 第三方工具：**cwRsync**（专为 Windows 优化）。

### **三、基本语法**

```
rsync [选项] [源路径] [目标路径]
```

**源路径和目标路径的形式**：

- **本地到本地**：

```
rsync /source/ /destination/
```

- **本地到远程**（通过 SSH）：

```
rsync /source/ user@host:/destination/
```

- **远程到本地**（通过 SSH）：

```
rsync user@host:/source/ /destination/
```

- **远程到远程**（需双方服务器支持 SSH 互访）：

```
rsync user1@host1:/source/ user2@host2:/destination/
```

### **四、常用选项**

#### **1. 传输控制**

| 选项       | 作用                                                        |
| ---------- | ----------------------------------------------------------- |
| -a         | 归档模式（递归 + 保留几乎所有文件属性），等价于 -rlptgoD。  |
| -v         | 详细模式，显示传输进度。                                    |
| -z         | 传输时压缩文件数据。                                        |
| -h         | 以人类可读的格式显示文件大小（如 1.2M）。                   |
| --progress | 显示详细的传输进度。                                        |
| -P         | 等价于 --partial --progress，保留部分传输的文件并显示进度。 |

#### **2. 过滤规则**

| 选项                | 作用                                                 |
| ------------------- | ---------------------------------------------------- |
| --exclude=PATTERN   | 排除匹配模式的文件 / 目录（如 --exclude=*.log）。    |
| --include=PATTERN   | 包含匹配模式的文件 / 目录（需配合 --exclude 使用）。 |
| --exclude-from=FILE | 从文件读取排除规则（每行一个模式）。                 |
| --delete            | 删除目标中源不存在的文件（同步删除操作）。           |

#### **3. 文件属性保留**

| 选项 | 作用                           |
| ---- | ------------------------------ |
| -r   | 递归复制目录。                 |
| -l   | 保留符号链接。                 |
| -p   | 保留文件权限。                 |
| -t   | 保留文件时间戳。               |
| -g   | 保留文件属组。                 |
| -o   | 保留文件属主（需 root 权限）。 |
| -D   | 保留设备文件和特殊文件。       |

#### **4. 连接与安全**

| 选项                 | 作用                                                         |
| -------------------- | ------------------------------------------------------------ |
| -e ssh               | 使用 SSH 作为传输协议（默认），可指定 SSH 选项（如 -e "ssh -p 2222"）。 |
| --rsync-path=PATH    | 指定远程服务器上 rsync 的路径（如 --rsync-path="/usr/bin/rsync"）。 |
| --password-file=FILE | 从文件读取 rsync 服务器密码（用于非 SSH 模式）。             |

### **五、常见场景示例**

#### **1. 本地文件同步**

```
# 将 /data/src 递归同步到 /data/dst（保留所有属性）
rsync -avz /data/src/ /data/dst/

# 只同步 .txt 文件，排除其他文件
rsync -avz --include="*.txt" --exclude="*" /data/src/ /data/dst/
```

#### **2. 通过 SSH 远程同步**

```
# 本地 → 远程
rsync -avz -e ssh /local/path/ user@remote:/remote/path/

# 远程 → 本地
rsync -avz -e ssh user@remote:/remote/path/ /local/path/

# 指定 SSH 端口
rsync -avz -e "ssh -p 2222" /local/path/ user@remote:/remote/path/
```

#### **3. 同步目录但排除特定文件**

```
# 排除所有 .log 文件和 tmp 目录
rsync -avz --exclude="*.log" --exclude="/tmp/" /source/ /destination/

# 从文件读取排除规则
rsync -avz --exclude-from='exclude_list.txt' /source/ /destination/
```

#### **4. 镜像目录（删除目标中不存在于源的文件）**

```
rsync -avz --delete /source/ /destination/
```

#### **5. 只更新比目标新的文件**

```
rsync -avzu /source/ /destination/  # -u 选项：update
```

#### **6. 断点续传大文件**

```
rsync -avzP /path/to/large_file user@remote:/path/to/
```

#### **7. 同步权限和时间戳**

```
rsync -a --no-perms --no-owner --no-group /source/ /destination/  # 选择性保留属性
```

### **六、高级用法**

#### **1. 使用 rsync 服务器模式**

1. **配置服务器（/etc/rsyncd.conf）**：

```
[backup]
path = /data/backup
comment = Backup Directory
read only = no
auth users = rsync-user
secrets file = /etc/rsyncd.secrets
```

1. **启动服务器**：

```
rsync --daemon
```

1. **客户端同步**：

```
rsync -avz rsync://user@server/backup/ /local/path/
```

#### **2. 高效备份重要目录**

```
# 每日增量备份（使用硬链接实现时间点快照）
rsync -avz --delete --link-dest=/backup/yesterday /source/ /backup/today/
```

#### **3. 同步时执行预处理 / 后处理**

```
# 同步前清理源目录
rsync -avz --delete --exclude="*.tmp" --exclude="cache/" /source/ /destination/

# 同步后执行脚本
rsync -avz /source/ /destination/ && /path/to/post_script.sh
```

### **七、性能优化建议**

1. **使用压缩**：对大文件或网络带宽有限的场景，添加 -z 选项。

1. **并行传输**：对大量小文件，考虑使用 parallel-rsync 或分割目录同步。

1. **减少校验开销**：通过 --size-only 仅比较文件大小（牺牲准确性换取速度）。

1. **使用** **-H** **保留硬链接**：避免重复传输相同内容。

1. **排除不必要的文件**：通过 --exclude 减少扫描范围。

### **八、注意事项**

1. **路径末尾的斜杠**：

```
rsync /source/ /destination/  # 将 source 目录内容复制到 destination 目录
rsync /source /destination/  # 将 source 目录本身复制到 destination 目录
```

1. **权限限制**：

- 普通用户无法保留文件属主（需 root 权限）。

- 使用 --no-owner 和 --no-group 选项避免权限问题。

1. **特殊文件处理**：

- 默认不处理设备文件，如需保留需添加 -D 选项。

1. **错误处理**：

- 使用 --dry-run 选项预览同步效果，避免意外删除。

- 添加 -n 选项模拟执行，不实际修改文件。

### **九、常见错误与解决**

1. **权限不足**：

```
# 错误：Permission denied
rsync -avz /root/secure/ /destination/  # 普通用户无法访问 /root

# 解决：使用 sudo
sudo rsync -avz /root/secure/ /destination/
```

1. **SSH 连接失败**：

```
# 错误：ssh: connect to host ... port 22: Connection refused
rsync -avz -e ssh user@host:/path/ /local/  # SSH 端口或服务问题

# 解决：检查 SSH 服务状态和端口
rsync -avz -e "ssh -p 2222" user@host:/path/ /local/
```

1. **文件时间戳差异导致重复同步**：

```
# 解决：使用 --checksum 强制比对文件内容
rsync -avz --checksum /source/ /destination/
```

### **十、替代工具**

- **scp**：简单的远程复制工具，但不支持增量传输。

- **unison**：双向文件同步工具，支持冲突检测和解决。

- **git**：代码版本控制工具，可用于跟踪文件变更。

- **borgbackup**：支持压缩、加密和增量备份的现代工具。

### **总结**

rsync 是一个功能强大、灵活高效的文件同步工具，适用于本地和远程场景。通过合理组合选项（如 -avz、--exclude、--delete），可以满足各种复杂的同步需求。在使用时需注意路径格式、权限设置和性能优化，以确保同步过程安全高效。