## Struct打包字节

### 简介
> Python 的 struct 模块是一个标准库模块，主要作用是 在 Python 的数据类型与二进制数据之间进行转换。
> 可以加字节序前缀来标识字节序，可选项为 <（小端）、>（大端）、!（网络字节序=大端）

### 大端序（Big-Endian）
- 高位字节放在低地址（前面）

- 低位字节放在高地址（后面）

- 直观理解就是 “人类习惯的书写顺序”：先写高位，再写低位
### 小端序（Little-Endian）

- 低位字节放在低地址（前面）

- 高位字节放在高地址（后面）

- 直观理解就是 “低位在前，高位在后”

### 类型
| 格式  | C 类型               | Python 类型         | 字节数 | 描述                           |
| --- | ------------------ | ----------------- | --- | ---------------------------- |
| `x` | pad byte           | 无                 | 1   | 填充字节，不存储数据                   |
| `c` | char               | bytes of length 1 | 1   | 单个字符                         |
| `b` | signed char        | int               | 1   | 有符号 8 位整数 (-128\~127)        |
| `B` | unsigned char      | int               | 1   | 无符号 8 位整数 (0\~255)           |
| `h` | short              | int               | 2   | 有符号 16 位整数                   |
| `H` | unsigned short     | int               | 2   | 无符号 16 位整数                   |
| `i` | int                | int               | 4   | 有符号 32 位整数                   |
| `I` | unsigned int       | int               | 4   | 无符号 32 位整数                   |
| `l` | long               | int               | 4   | 有符号 32 位整数                   |
| `L` | unsigned long      | int               | 4   | 无符号 32 位整数                   |
| `q` | long long          | int               | 8   | 有符号 64 位整数                   |
| `Q` | unsigned long long | int               | 8   | 无符号 64 位整数                   |
| `f` | float              | float             | 4   | 单精度浮点数                       |
| `d` | double             | float             | 8   | 双精度浮点数                       |
| `s` | char\[]            | bytes             | n   | 固定长度字符串，例如 `'5s'` 表示 5 字节字符串 |
| `p` | char\[]            | bytes             | n   | Pascal 风格字符串，第一个字节表示长度       |
| `?` | \_Bool             | bool              | 1   | 布尔值                          |


### 示例一
> 有type,version,size,data四个字段，分别对应4字节，1字节，4字节，任意字节。其中type和version为头部信息，size为数据长度，data为数据。
```
import struct

version = 1
type=1
data = "hello"
size = len(data)


init_head = struct.pack('>IB', type, version)
data_length = struct.pack('>I', size)

# 组合数据
all_data = init_head + data_length + data.encode("utf-8")

# 解包
# I 长度为4，B长度为1，所以这两个结合起来为5字节
init_head = struct.unpack('>IB', all_data[:5])
data_length = struct.unpack('>I', all_data[5:9])
data = all_data[9:]
```

### 示例二
> 有version和type两个字段，一共占用1个字节,version 占用6bit,type 占用2bit

```
import struct

version = 25
type=5

# 将version和type合并为1个字节
merge_data = struct.pack('B', (version << 2) | type)
# 解包
type = merge_data >> 2
# 这个11指的是掩码，因为低位占2位，所以是两个1，如果是4位，那就是0xF（可以用二进制，也可以用16进制）
version = merge_data & 0x11
```
### 示例二的合并与解包过程
```
# 合并步骤
# 步骤1:将version 转成二进制
25 = 0001 1001
# 步骤2:将type 转成二进制
3 = 0000 0011
# 步骤3:采用的大端序，高位在前，低位在后，type作为低位，需要2bit，所以version左移2位
25 << 2 = 100 = 0110 0100
# 步骤4:合并
0110 0100 | 0000 0011 = 0110 0111

# 解包步骤
# 步骤1:将合并后的数据右移2位，将version取出
0110 0111 >> 2 = 0001 1001 = 25
# 步骤2:获取type
0110 0111 & 0000 0011 = 0000 0011 = 3
```