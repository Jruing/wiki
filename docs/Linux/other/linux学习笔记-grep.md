以下是 **`grep`** 的简明中文手册，涵盖基本用法、常用选项、正则表达式、以及实战示例。`grep` 是 Linux/Unix 中最常用的文本搜索工具之一，用于在文件中查找特定的字符串或模式。

---

# 📘 grep 手册（中文版）

## 一、简介

`grep`（Global Regular Expression Print）是一个强大的命令行工具，用于在文件中搜索匹配指定**模式**的文本行，并将这些行输出到终端或其他命令中。

```bash
grep [选项] '搜索模式' 文件名
```

或者从管道输入：

```bash
command | grep '搜索模式'
```

---

## 二、基本语法与示例

### 基本用法

```bash
grep 'hello' file.txt         # 搜索包含 "hello" 的行
grep -i 'hello' file.txt      # 忽略大小写搜索
grep -v 'error' file.txt      # 反向匹配：显示不包含 "error" 的行
grep -n 'warning' file.txt    # 显示匹配行及其行号
grep -c 'success' file.txt    # 统计匹配的行数
grep -l 'TODO' *.txt          # 只显示包含 "TODO" 的文件名
```

---

## 三、常用选项（Options）

| 选项 | 说明 |
|------|------|
| `-i` | 忽略大小写（ignore case） |
| `-v` | 反向匹配（invert match） |
| `-n` | 显示匹配行的行号 |
| `-c` | 输出匹配行的数量 |
| `-l` | 仅输出匹配的文件名 |
| `-r` 或 `--recursive` | 递归搜索子目录中的文件 |
| `-h` | 不显示文件名 |
| `-m NUM` | 最多匹配 NUM 行后停止 |
| `-A NUM` | 匹配行后显示 NUM 行（After） |
| `-B NUM` | 匹配行前显示 NUM 行（Before） |
| `-C NUM` | 匹配行前后各显示 NUM 行（Context） |
| `-E` | 启用扩展正则表达式（相当于 egrep） |
| `-F` | 将搜索词视为固定字符串，而不是正则表达式（相当于 fgrep） |

---

## 四、正则表达式支持

默认使用 **基础正则表达式（BRE）**，若要使用更强大的正则语法，请加上 `-E` 选项。

### 常见正则符号

| 正则 | 含义 |
|------|------|
| `.` | 匹配任意单个字符 |
| `^` | 匹配行首 |
| `$` | 匹配行尾 |
| `*` | 前一个字符出现 0 次或多次 |
| `+` | 前一个字符出现 1 次或多次（需 `-E`） |
| `?` | 前一个字符出现 0 次或 1 次（需 `-E`） |
| `{n,m}` | 前一个字符出现 n 到 m 次（需 `-E`） |
| `[]` | 匹配括号内的任意一个字符 |
| `[^]` | 匹配不在括号内的任意一个字符 |
| `\b` | 单词边界 |
| `()` | 分组（需 `-E`） |
| `|` | 或操作（需 `-E`） |

---

## 五、实战示例

### 示例 1：查找 IP 地址

```bash
grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}' file.log
```

### 示例 2：查找邮箱地址

```bash
grep -E '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' file.txt
```

### 示例 3：递归查找当前目录下所有 .log 文件中含 "error" 的行

```bash
grep -r 'error' . --include='*.log'
```

### 示例 4：显示匹配行及其上下文（前 2 行、后 3 行）

```bash
grep -B2 -A3 'fatal' error.log
```

### 示例 5：统计日志中每个 IP 出现的次数

```bash
grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' access.log | sort | uniq -c | sort -nr
```

---

## 六、grep 家族命令对比

| 命令 | 功能 | 说明 |
|------|------|------|
| `grep` | 使用基础正则表达式 |
| `egrep` | 使用扩展正则表达式（相当于 `grep -E`） |
| `fgrep` | 快速搜索固定字符串（相当于 `grep -F`） |
| `pgrep` | 查找进程 ID（不属于文本搜索） |

---

## 七、注意事项

- 使用 `-i` 忽略大小写时，注意性能可能略有下降。
- 使用 `-r` 递归搜索时建议配合 `--include` 或 `--exclude` 控制范围。
- 如果只是匹配固定字符串，使用 `-F` 更高效。
- 在脚本中使用 `grep` 时，可检查返回值判断是否找到匹配项：
  ```bash
  if grep -q 'pattern' file; then
      echo "Found"
  else
      echo "Not found"
  fi
  ```

---

## 八、参考资料

- `man grep`
- GNU grep 官方文档：https://www.gnu.org/software/grep/manual/
- 《Linux Command Line and Shell Scripting Bible》

