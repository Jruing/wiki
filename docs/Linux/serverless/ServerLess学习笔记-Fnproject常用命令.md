# ServerLess学习笔记-FnProject常用命令

## 启动/停止

```
# 启动
fn start
# 停止
fn stop
```

## 创建

```
[root@VM-24-9-centos serverless]# fn create

MANAGEMENT COMMAND
  fn create -   Create a new object
                               
USAGE
  fn [global options] create [command options] <object-type>
    
DESCRIPTION
  This command creates a new object ('app', 'context', 'function', or 'trigger').
    
SUBCOMMANDS
  app, apps, a               创建应用
  context, ctx               创建
  function, func, f, fn      为一个应用创建一个函数
  trigger, trig, t, tr       创建一个触发器
  help, h                    Shows a list of commands or help for one command
                         
COMMAND OPTIONS
  --help, -h  show help

FURTHER HELP:  See 'fn create <subcommand> --help' for more information about a command.
```

## 查询

```
[root@VM-24-9-centos serverless]# fn list

MANAGEMENT COMMAND
  fn list -   Return a list of created objects
                             
USAGE
  fn [global options] list [command options] <subcommand>
    
DESCRIPTION
  This command returns a list of created objects ('app', 'call', 'context', 'function' or 'trigger') or configurations.
    
SUBCOMMANDS
  apps, app, a                 列出所有创建的应用
  config, config, cf           列出应用的配置
  contexts, context, ctx       列出上下文
  functions, funcs, f, fn      列出应用关联的函数
  triggers, trigs, t, tr       列出所有的触发器
  help, h                      Shows a list of commands or help for one command
                           
COMMAND OPTIONS
  --help, -h  show help

FURTHER HELP:  See 'fn list <subcommand> --help' for more information about a command.

```



- 查询函数详情`fn inspect function <app-name> <function-name>`

    ```
    [root@VM-24-9-centos fn_demo]# fn inspect function fn_app fn_demo
    {
    	"annotations": {
    		"fnproject.io/fn/invokeEndpoint": "http://localhost:8080/invoke/01HD5Z2WFTNG8G00RZJ0000002" # 函数实际调用地址
    	},
    	"app_id": "01HD5YZTVENG8G00RZJ0000001",
    	"created_at": "2023-10-20T07:16:36.474Z",
    	"id": "01HD5Z2WFTNG8G00RZJ0000002",
    	"idle_timeout": 30,
    	"image": "fn_demo:0.0.2",
    	"memory": 256,
    	"name": "fn_demo",
    	"timeout": 30,
    	"updated_at": "2023-10-20T07:16:36.474Z"
    }
    ```

## 删除

    [root@VM-24-9-centos serverless]# ./fn delete
    
    MANAGEMENT COMMAND
      fn delete -   Delete an object
                                   
    USAGE
      fn [global options] delete [command options] <subcommand>
        
    DESCRIPTION
      This command deletes a created object ('app', 'context', 'function' or 'trigger').
        
    SUBCOMMANDS
      app, apps, a               删除应用
      config, config, cf         删除应用关联函数的配置
      context, ctx               删除上下文
      function, func, f, fn      删除应用的一个函数
      trigger, trig, t, tr       删除触发器
      help, h                    Shows a list of commands or help for one command
                             
    COMMAND OPTIONS
      --help, -h  show help
    
    FURTHER HELP:  See 'fn delete <subcommand> --help' for more information about a command.

## 调用

### 通过CLI调用

```
fn invoke <app-name> <function-name>
```

### 通过Curl调用

```
curl -X "POST" -H "Content-Type: application/json" http://localhost:8080/invoke/01DJRP8FT8NG8G00GZJ0000002
```

