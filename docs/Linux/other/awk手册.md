以下是 **`awk`** 的简明中文手册，涵盖基本语法、常用命令、内置变量、函数以及实战示例。`awk` 是一种强大的文本处理语言，尤其适合对结构化数据（如日志、CSV、TSV 等）进行分析和格式化输出。

---

# 📘 awk 手册（中文版）

## 一、简介

`awk` 是一种模式扫描和处理语言，用于对文本文件逐行进行操作。其命名来自三位作者：Alfred Aho、Peter Weinberger 和 Brian Kernighan。

```bash
awk [选项] '模式 {动作}' 文件名
```

或者：

```bash
command | awk '模式 {动作}'
```

---

## 二、基本结构

### 1. 格式

```bash
awk '/pattern/ {action}' file.txt
```

- `/pattern/`：匹配的模式（可选）
- `{action}`：执行的动作（默认是打印整行）

### 2. 示例

```bash
awk '{print $0}' file.txt   # 打印整行
awk '{print $1}' file.txt   # 打印第一列
```

---

## 三、常用内置变量

| 变量 | 含义 |
|------|------|
| `$0` | 当前行的完整内容 |
| `$1`, `$2`, ... | 第 1、2、... 列的内容 |
| `NF` | 当前行的字段数（列数） |
| `NR` | 已读取的记录号（行号） |
| `FNR` | 当前文件的行号（多个文件时独立计数） |
| `FS` | 输入字段分隔符，默认为空格或制表符 |
| `OFS` | 输出字段分隔符，默认空格 |
| `RS` | 输入记录分隔符，默认换行符 |
| `ORS` | 输出记录分隔符，默认换行符 |
| `FILENAME` | 当前输入文件名 |

---

## 四、常用命令与技巧

### 1. 指定字段分隔符

```bash
awk -F ',' '{print $1}' file.csv      # 使用逗号作为分隔符
awk -F '\t' '{print $2}' file.tsv     # 使用制表符作为分隔符
```

或者在脚本中设置：

```bash
awk 'BEGIN{FS=","} {print $1}' file.csv
```

---

### 2. 打印特定行

```bash
awk 'NR == 3' file.txt         # 打印第3行
awk 'NR >= 2 && NR <=5' file.txt  # 打印第2到第5行
```

---

### 3. 条件判断

```bash
awk '$3 > 100' file.txt        # 打印第三列大于100的行
awk '$2 == "error"' file.txt   # 打印第二列等于"error"的行
```

---

### 4. 计算总和、平均值等

```bash
awk '{sum += $1} END {print sum}' file.txt  # 求第一列总和
awk '{sum += $1} END {print sum/NR}' file.txt  # 求平均值
```

---

### 5. 统计出现次数

```bash
awk '{count[$1]++} END {for (key in count) print key, count[key]}' file.txt
```

这个命令会统计第一列每个值出现的次数。

---

### 6. 多文件处理

```bash
awk 'NR==FNR {a[$1]; next} $1 in a' file1.txt file2.txt
```

- `NR==FNR` 表示正在处理第一个文件。
- 此命令可用于找出两个文件中第一列相同的行。

---

### 7. 修改内容并输出

```bash
awk '{$3 = $3 * 2; print}' file.txt   # 将第三列翻倍后输出
```

---

## 五、流程控制语句

### if 判断

```bash
awk '{if ($3 > 90) print $1, "优秀"; else print $1, "及格"}' file.txt
```

### for 循环

```bash
awk '{for(i=1; i<=NF; i++) print $i}' file.txt   # 打印每一列
```

---

## 六、函数支持

### 内置函数

- `length($0)`：返回当前行长度
- `substr(s, i, l)`：从字符串 s 的第 i 个位置开始截取长度为 l 的子串
- `index(s, t)`：返回 t 在 s 中的位置，不存在则返回 0
- `split(s, arr, sep)`：将字符串 s 按 sep 分割到数组 arr 中
- `match(s, r)`：匹配正则表达式 r，成功返回起始位置
- `tolower()` / `toupper()`：大小写转换

### 自定义函数（GNU awk 支持）

```bash
awk '
function square(x) {
    return x*x
}
{print square($1)}
' file.txt
```

---

## 七、实战示例

### 示例 1：提取访问日志中的 IP 地址（假设 IP 是第一列）

```bash
awk '{print $1}' access.log
```

### 示例 2：查找最大值

```bash
awk 'NR == 1 || $1 > max {max = $1} END {print max}' file.txt
```

### 示例 3：合并多列

```bash
awk '{print $1, $2, $3}' file.txt
```

### 示例 4：按条件过滤 + 输出新列

```bash
awk '$3 > 100 {print $1, $2, "达标"}' file.txt
```

---

## 八、注意事项

- `awk` 默认以空白字符（空格或 tab）分割字段。
- 如果你使用 macOS 或其他非 GNU 系统，请注意某些高级功能可能不支持。
- 推荐使用 `gawk`（GNU awk），功能更强大。
- 对于大型文件，`awk` 性能通常优于 Python 脚本。

---

## 九、参考资料

- `man awk`
- 《The AWK Programming Language》by Alfred V. Aho et al.
- GNU Awk 用户指南：https://www.gnu.org/software/gawk/manual/
