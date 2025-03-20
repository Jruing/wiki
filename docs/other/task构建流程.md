# 简介
> Task 是一个任务运行器/构建工具，旨在更简单、更易于使用 比 GNU Make 更重要。
> 官网地址：https://taskfile.dev/
# 创建一个taskfile文件
```
task --init 
```
# 调用任务
> task 任务名称
```
task default 
```
# 添加一个构建任务
```
version: '3'


# 任务项
tasks:
  # 任务描述
  desc: "这是一个demo"
  # 任务摘要
  summary: |
    这是一个任务摘要
  # 任务名称,默认任务为default
  default: 
    # 命令
    cmds: 
      - echo "Hello, World!"
  # 增加一个构建任务
  build:
    cmds:
      - echo "开始构建"
```

# 读取变量/环境变量

```
version: '3'

# 设置全局环境变量
env:
  Name: "task"

# 任务项
tasks:
  # 任务名称,默认任务为default
  default: 
    # 命令
    cmds: 
      - echo "Hello, World!"
  demo1:
    # 设定必选参数
    require:
      vars: [Name]
    # 手动定义变量
    vars:
      Name: "demo1"
    # 读取.env文件中的环境变量
    dotenv: [".env"]
    # 设置局部环境变量
    env:
      JobName: "demo1"
    cmds: 
      # 引用环境变量
      - echo $JobName
      # 引用手动定义的变量
      - echo {{.Name}}
```

# 调用其他的任务

```
version: '3'

# 任务项
tasks:
  # 任务名称,默认任务为default
  default: 
    # 命令
    cmds: 
      - echo "Hello, World!"
  demo1:
    cmds: 
      - echo "demo1"
  demo2:
    cmds: 
      - echo "demo2"
  demo3:
    cmds:
      # task用于调用其他任务
      - task: demo1
      - task: demo2
      - echo "demo3"
```

# 获取操作系统类型

> {{OS}} 是获取当前操作系统类型

```
version: '3'

# 任务项
tasks:
  # 任务名称,默认任务为default
  default: 
    # 命令
    cmds: 
      - echo "Hello, World!"
  demo1:
    # 限定操作系统或架构
    platforms: [windows,amd64]
    cmds: 
      - echo “当前操作系统：{{OS}}”
```

# 导入其他任务文件

## Taskfile.yml

```
version: '3'

includes:
  lib:
    # 其他任务文件路径
    taskfile: ./demo1/Taskfile1.yml
    # 将上面任务文件内容拉入当前任务文件
    flatten: true
    # 可选，若上面声明的任务文件不存在，是否忽略错误
    optional: true

# 任务项
tasks:
  # 任务名称,默认任务为default
  default: 
    # 命令
    cmds: 
      - echo "Hello, World!"
  demo1:
    cmds: 
      - echo “当前操作系统：{{OS}}” 
      - task demo2
```

## Taskfile2.yml
```
version: '3'

# 任务项
tasks:
  demo2:
    cmds: 
      - echo “demo2:当前操作系统：{{OS}}”
```

## 测试

```
# 获取当前任务文件所有的任务名称（包含加载的其他任务文件中的任务）
task -a
```

# 任务别名

```
version: '3'

tasks:
  build:
    cmds:
      - task: build-win
      - task: build-lx
  build-windows:
    # 给当前任务定义一个别名，其他任务可以通过别名调用这个任务
    aliases: [build-win]
    cmds:
      - echo "开始构建windows环境"
  
  build-linux:
    # 给当前任务定义一个别名，其他任务可以通过别名调用这个任务
    aliases: [build-lx]
    cmds:
      - echo "开始构建linux环境"
```

# 用户提示

```
version: '3'

# 任务项
tasks:
  demo1:
    prompt: "当前操作系统:{{OS}},请确定是否执行"
    cmds: 
      - echo “demo2:当前操作系统：{{OS}}”
```

# 静音模式

```
version: '3'

# 任务项
tasks:
  demo1:
    prompt: "当前操作系统:{{OS}},请确定是否执行"
    cmds: 
      - echo “demo2:当前操作系统：{{OS}}”
```

# 服务依赖

```
version: '3'

# 任务项
tasks:
  # 任务名称,默认任务为default
  default: 
    # 命令
    cmds: 
      - echo "Hello, World!"
  demo1:
    # 依赖前置任务
    deps: [demo2]
    cmds: 
      - echo "demo1"
  demo2:
    cmds: 
      - echo "demo2"
  demo3:
    cmds:
      - echo "demo3"
```

# 忽略异常

```
version: '3'

# 任务项
tasks:
  # 任务名称,默认任务为default
  default: 
    # 命令
    cmds: 
      - echo "Hello, World!"
  demo1:
    cmds: 
      - echo "demo1"
  demo2:
    cmds: 
      - echo "demo2"
  demo3:
    cmds:
      # task用于调用其他任务
      - task: demo1
        # 忽略异常，继续执行
        ignore_error: true
      - task: demo2
      - echo "demo3"
```

# 指定任务执行目录

```
version: '3'

# 任务项
tasks:
  restart_nginx:
    # 指定nginx所在目录
    dir: /home/nginx
    cmds: 
      - nginx -s reload
```

# 循环

```
version: '3'

tasks:
  default:
    cmds:
      # 循环列表
      - for: ['foo.txt', 'bar.txt']
        # .ITEM代表循环的某一项
        cmd: cat {{ .ITEM }}
```



