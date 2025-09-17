`jq` 是一个轻量级且强大的命令行 JSON 处理工具，它可以让你在 Linux 终端中轻松地解析、过滤、修改和操作 JSON 数据。`jq` 的语法类似于 `sed` 或 `awk`，但专门用于 JSON。

---

## **1. 安装 `jq`**

### **Ubuntu/Debian**
```bash
sudo apt-get install jq
```

### **CentOS/RHEL**
```bash
sudo yum install jq
# 或者使用 dnf
sudo dnf install jq
```

### **macOS (Homebrew)**
```bash
brew install jq
```

### **验证安装**
```bash
jq --version
```

---

## **2. `jq` 的基本用法**

`jq` 的基本语法是：
```bash
jq [options] <jq-filter> [file]
```

- **`<jq-filter>`**: 用于处理 JSON 的过滤器。
- **`[file]`**: 输入的 JSON 文件（如果未提供，则从标准输入读取）。

### **2.1 最简单的例子：格式化 JSON**

```bash
echo '{"name":"Alice","age":30}' | jq '.'
```

输出：
```json
{
  "name": "Alice",
  "age": 30
}
```

> **说明**：`jq '.'` 表示输出整个 JSON 对象。

---

## **3. 提取 JSON 字段**

### **3.1 提取单个字段**

```bash
echo '{"name":"Alice","age":30}' | jq '.name'
```

输出：
```json
"Alice"
```

> **注意**：输出是 JSON 字符串，所以字段值是带引号的。

### **3.2 提取多个字段**

```bash
echo '{"name":"Alice","age":30}' | jq '{name: .name, age: .age}'
```

输出：
```json
{
  "name": "Alice",
  "age": 30
}
```

### **3.3 提取数组元素**

```bash
echo '{"users":["Alice","Bob"]}' | jq '.users[0]'
```

输出：
```json
"Alice"
```

### **3.4 提取嵌套字段**

```bash
echo '{"person":{"name":"Alice","age":30}}' | jq '.person.name'
```

输出：
```json
"Alice"
```

### **3.5 提取数组的所有元素**

```bash
echo '{"users":["Alice","Bob"]}' | jq '.users[]'
```

输出：
```json
"Alice"
"Bob"
```

---

## **4. 过滤和条件查询**

### **4.1 过滤数组（`select`）**

```bash
echo '[{"name":"Alice","age":30},{"name":"Bob","age":20}]' | jq '.[] | select(.age > 25)'
```

输出：
```json
{
  "name": "Alice",
  "age": 30
}
```

### **4.2 过滤多个条件**

```bash
echo '[{"name":"Alice","age":30,"city":"Beijing"},{"name":"Bob","age":20,"city":"Shanghai"}]' | jq '.[] | select(.age > 20 and .city == "Beijing")'
```

输出：
```json
{
  "name": "Alice",
  "age": 30,
  "city": "Beijing"
}
```

### **4.3 正则匹配（`test`）**

```bash
echo '[{"name":"Alice","age":30},{"name":"Bob","age":20}]' | jq '.[] | select(.name | test("^A"))'
```

输出：
```json
{
  "name": "Alice",
  "age": 30
}
```

---

## **5. 修改 JSON 数据**

### **5.1 修改字段值**

```bash
echo '{"name":"Alice","age":30}' | jq '.name = "Bob"'
```

输出：
```json
{
  "name": "Bob",
  "age": 30
}
```

### **5.2 添加字段**

```bash
echo '{"name":"Alice","age":30}' | jq '.city = "Beijing"'
```

输出：
```json
{
  "name": "Alice",
  "age": 30,
  "city": "Beijing"
}
```

### **5.3 删除字段**

```bash
echo '{"name":"Alice","age":30,"city":"Beijing"}' | jq 'del(.city)'
```

输出：
```json
{
  "name": "Alice",
  "age": 30
}
```

### **5.4 修改数组**

```bash
echo '{"users":["Alice","Bob"]}' | jq '.users |= . + ["Charlie"]'
```

输出：
```json
{
  "users": [
    "Alice",
    "Bob",
    "Charlie"
  ]
}
```

---

## **6. 高级用法**

### **6.1 遍历数组（`map`）**

```bash
echo '[{"name":"Alice","age":30},{"name":"Bob","age":20}]' | jq 'map(.age)'
```

输出：
```json
[
  30,
  20
]
```

### **6.2 合并数组**

```bash
echo '[{"name":"Alice"},{"name":"Bob"}]' | jq '.[0] + .[1]'
```

输出：
```json
{
  "name": "Bob"
}
```

### **6.3 计算字段值**

```bash
echo '{"values":[1,2,3,4,5]}' | jq '.values | add'
```

输出：
```json
15
```

### **6.4 排序**

```bash
echo '{"values":[5,2,4,1,3]}' | jq '.values | sort'
```

输出：
```json
[
  1,
  2,
  3,
  4,
  5
]
```

### **6.5 去重**

```bash
echo '{"values":[1,2,2,3,3,3]}' | jq '.values | unique'
```

输出：
```json
[
  1,
  2,
  3
]
```

---

## **7. 输出格式控制**

### **7.1 输出为紧凑格式（`-c`）**

```bash
echo '{"name":"Alice","age":30}' | jq -c '.'
```

输出：
```json
{"name":"Alice","age":30}
```

### **7.2 输出为字符串（`-r`）**

```bash
echo '{"name":"Alice","age":30}' | jq -r '.name'
```

输出：
```
Alice
```

> **说明**：`-r` 表示输出原始字符串（不带引号）。

### **7.3 输出为 CSV**

```bash
echo '[{"name":"Alice","age":30},{"name":"Bob","age":20}]' | jq -r '.[] | [.name, .age] | @csv'
```

输出：
```csv
"Alice",30
"Bob",20
```

---

## **8. 从文件读取 JSON**

### **8.1 读取文件**

```bash
jq '.name' data.json
```

### **8.2 读取多个文件**

```bash
jq '.name' file1.json file2.json
```

### **8.3 从标准输入读取**

```bash
cat data.json | jq '.name'
```

---

## **9. 错误处理**

### **9.1 忽略错误（`//`）**

```bash
echo '{"name":"Alice"}' | jq '.age // "Unknown"'
```

输出：
```
"Unknown"
```

### **9.2 检查字段是否存在**

```bash
echo '{"name":"Alice"}' | jq 'if .age then .age else "Unknown" end'
```

输出：
```
"Unknown"
```

---

## **10. 实用示例**

### **10.1 解析 Docker inspect 输出**

```bash
docker inspect my_container | jq '.[0].NetworkSettings.IPAddress'
```

### **10.2 解析 Kubernetes 配置**

```bash
kubectl get pods -o json | jq '.items[].metadata.name'
```

### **10.3 解析 API 响应**

```bash
curl -s 'https://api.github.com/users/octocat' | jq '.name'
```

### **10.4 批量处理 JSON 文件**

```bash
for file in *.json; do
  jq '.name' "$file"
done
```

---

## **11. 常见问题**

### **11.1 `jq: error: Cannot index array with string`**

- **原因**：试图用字符串索引数组。
- **解决**：使用 `.[]` 遍历数组，或者用数字索引 `.users[0]`。

### **11.2 `jq: error: Invalid numeric literal`**

- **原因**：JSON 格式错误（如未闭合的引号）。
- **解决**：检查输入 JSON 是否正确。

---

## **总结**

`jq` 是一个功能强大的 JSON 处理工具，适用于：
- 解析 API 响应
- 处理配置文件
- 日志分析
- 自动化脚本

