# MCP从零到一

## 简述

> MCP 是一个开放协议，它为应用程序向 LLM 提供上下文的方式进行了标准化。你可以将 MCP 想象成 AI 应用程序的 USB-C 接口。就像 USB-C 为设备连接各种外设和配件提供了标准化的方式一样，MCP 为 AI 模型连接各种数据源和工具提供了标准化的接口。

## MCP通用架构

*架构图来自官网*

![image-20250508142533153](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250508142533153.png)

- **MCP Hosts**: 如 Claude Desktop、IDE 或 AI 工具，希望通过 MCP 访问数据的程序
- **MCP Clients**: 维护与服务器一对一连接的协议客户端
- **MCP Servers**: 轻量级程序，通过标准的 Model Context Protocol 提供特定能力
- **本地数据源**: MCP 服务器可安全访问的计算机文件、数据库和服务
- **远程服务**: MCP 服务器可连接的互联网上的外部系统（如通过 APIs）

## 名词概念

- 工具(tool)：使服务器能够向客户端暴露可执行的功能。通过工具，LLMs可以与外部系统交互、执行计算并在现实世界中采取行动。
- 资源(resource)：是MCP中用来对外暴露数据的核心机制，你可以把它想象成一个只读的数据库接口或者文件系统，比如日志文件
- 提示(prompt)：提供预定义的交互模式或者推理指引。

## 准备工作

- CherryStudio

- Python

- VScode

## CherryStudio配置

### 基础配置

![image-20250508140329376](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250508140329376.png)

### MCP服务器配置(自有MCP服务)

![image-20250508140512173](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250508140512173.png)

![image-20250508140833504](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250508140833504.png)

![image-20250508143141889](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250508143141889.png)

### MCP服务器配置(公网MCP服务)

![image-20250508141159426](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250508141159426.png)

## 环境准备

### 创建项目文件夹

```
mkdir mcp_server_demo
cd mcp_server_demo
```

### 创建虚拟环境

```
python -m venv .venv
cd .venv
cd Scripts
# 激活虚拟环境
activate
```

### 安装依赖

```
pip install mcp
pip install mcp[cli]
```

## 栗子

### data.json

```
{
    "Inbound": 0,
    "Outbound": 0,
    "Inventory": 0
}
```

### main.py

```
# encoding: utf-8
from mcp.server.fastmcp import FastMCP
import json
# 创建一个FastMCP服务
mcp = FastMCP("Demo", "This is a demo server")
def load_data():
    with open("data.json",'r',encoding="utf-8") as f:
        return json.loads(f.read())

@mcp.tool(name="入库",description="入库多少商品")
def Inbound(num:int) -> dict:
    data = load_data()
    data["Inbound"] += num
    data['Inventory'] = data["Inbound"]-data["Outbound"]
    with open("data.json","w") as f:
        f.write(json.dumps(data))
    return data

@mcp.tool(name="出库",description="出库多少商品")
def Outbound(num:int) -> dict|str:
    """Add two numbers"""
    data = load_data()
    data["Outbound"] += num
    if num > data["Inbound"]:
        return "库存不足"
    data['Inventory'] = data["Inbound"]-data["Outbound"]
    with open("data.json","w") as f:
        f.write(json.dumps(data))
    return data

@mcp.prompt(name="展示仓库信息",description="展示仓库信息")
async def prompt() -> str:
    """Prompt for a string"""
    status = await load_data()
    return f"""
        入库数量:{status["Inbound"]}
        出库数量:{status["Outbound"]}
        库存数量:{status["Inventory"]}
    """

@mcp.resource("accounting://status",name="库存",description="库存信息")
async def resource() -> dict:
    """Return a text resource"""
    data = await load_data()
    return data
if __name__ == "__main__":
    mcp.run("sse")
```



## 本地测试

```
mcp dev main.py
# 访问http://127.0.0.1:6274/#resources
```

### tool

> 工具：提供了出库与入库两个工具，根据用户输入的内容结合大模型理解，调用相对应的工具进行入库与出库，结果持久化存储在json文件中

![image-20250508154539296](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250508154539296.png)

![image-20250508154643185](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250508154643185.png)

### resource

> 资源：用户可以检索仓库的最新状态，包括入库，出库，库存

![image-20250508154732223](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250508154732223.png)

### Prompt

> 提示：负责将仓库的状态格式化为易读的报告

![image-20250508154814802](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250508154814802.png)

## 正式使用

### 配置MCP服务

![image-20250508161359897](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250508161359897.png)

### 选择MCP服务

![image-20250508161421722](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250508161421722.png)

### 选择资源

![image-20250508161451710](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250508161451710.png)

### 结果验证

![image-20250508165002875](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250508165002875.png)

![image-20250508165018685](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250508165018685.png)