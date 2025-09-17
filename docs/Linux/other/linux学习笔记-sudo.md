
## 1. sudo是什么

`sudo`（superuser do）是 Linux/Unix 系统中用来**以超级用户（root）或其他指定用户身份执行命令**的工具。

* 普通用户通过 `sudo` 获得临时的管理员权限，避免直接使用 root 账号。
* 使用 `sudo` 能提升系统安全性，减少误操作风险。

---

## 2. 原理是什么

`sudo` 的核心原理是：

1. **配置文件控制权限**

   * `sudo` 通过 `/etc/sudoers` 配置文件，定义哪些用户可以在什么条件下，以什么身份执行哪些命令。
   * 使用 `visudo` 工具修改配置文件，避免语法错误。

2. **认证机制**

   * 用户在执行 `sudo` 时，必须输入自己的密码（而非 root 密码）。
   * 密码验证成功后，在一段时间内（默认 5 分钟）不必重复输入。

3. **权限提升流程**

   * `sudo` 会检查调用者是否在 `sudoers` 配置中有权限。
   * 符合条件时，`sudo` 使用 **setuid** 技术临时提升进程权限，以 root 或指定用户身份运行目标命令。

---

## 3. 可配置项有哪些

常见可配置项主要在 `/etc/sudoers` 中：

* **用户与命令规则**

  ```
  user host = (runas_user) command_list
  ```

  * `user`：指定哪个用户
  * `host`：在哪些主机上生效
  * `(runas_user)`：以哪个用户身份执行（默认 root）
  * `command_list`：允许执行的命令

* **别名（简化配置）**

  * `User_Alias`：用户别名
  * `Host_Alias`：主机别名
  * `Cmnd_Alias`：命令别名

* **NOPASSWD**

  * 允许某些命令在执行时免密码验证，例如：

    ```
    user ALL=(ALL) NOPASSWD:/usr/bin/systemctl restart nginx
    ```

* **Defaults 配置项**

  * 控制 sudo 的行为，比如：

    * `Defaults timestamp_timeout=10`（密码有效期 10 分钟）
    * `Defaults logfile="/var/log/sudo.log"`（记录日志文件）
    * `Defaults requiretty`（要求通过终端运行 sudo）

---

## 4. 注意事项

1. **不要直接编辑 `/etc/sudoers`**，应使用 `visudo`，它会检查语法，避免导致无法使用 sudo。
2. **限制用户权限**，只赋予必要的命令执行权限，避免使用 `ALL=(ALL) ALL` 给所有权限。
3. **日志审计**，开启日志记录，方便审计用户的 sudo 操作。
4. **有效期与安全**，合理配置 `timestamp_timeout`，防止长时间保持高权限。
5. **免密码执行要谨慎**，避免出现安全漏洞。

---

## 5. 实践案例

### 案例1：允许用户执行所有命令

```bash
# 在 sudoers 文件中加入
jruing ALL=(ALL) ALL
```

效果：用户 `jruing` 可以使用 `sudo` 执行任意命令。

---

### 案例2：只允许重启 Nginx 服务

```bash
jruing ALL=(ALL) NOPASSWD:/usr/bin/systemctl restart nginx
```

效果：用户 `jruing` 可以不输入密码直接重启 nginx，但不能执行其他命令。

---

### 案例3：限制日志与时间

```bash
Defaults logfile="/var/log/sudo.log"
Defaults timestamp_timeout=2
```

效果：

* 所有 sudo 操作会记录到 `/var/log/sudo.log`。
* 用户输入密码后，仅 2 分钟有效，之后需要再次输入。
