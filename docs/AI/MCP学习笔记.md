# MCP学习笔记

## 介绍

MCP 是一种开放协议，它标准化了应用程序如何为 LLM 提供上下文。将 MCP 想象成 AI 应用程序的 USB-C 端口。正如 USB-C 提供了一种将设备连接到各种外围设备和配件的标准化方式一样，MCP 也提供了一种将 AI 模型连接到不同数据源和工具的标准化方式。

官网地址: https://modelcontextprotocol.io/introduction

## 前置条件

LLM客户端：vscode，cline插件

## 编写服务端栗子

```
# weather.py
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# 初始化FastMCP服务
mcp = FastMCP("LiteTools")


async def get_weatcher(city:str,area:str) ->  Any:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://cn.apihz.cn/api/tianqi/tqyb.php?id=88888888&key=88888888&sheng={city}&place={area}")
        return resp.json()
def format_weather(data:Any) -> str:
    info = f"""
地点: {data['place']}
降雨量: {data['precipitation']}
温度: {data['temperature']}
湿度: {data['humidity']}
风向: {data['windDirection']}
风速: {data['windSpeed']}
天气: {data['weather1']}"""
    print(info)
    return info

@mcp.tool()
async def get_weather_tools(city:str,area:str) -> str:
    """
    Args:
        city: 城市,省或者直辖市
        area: 地区或者地级市
    """
    data = await get_weatcher(city,area)
    return format_weather(data)
if __name__ == "__main__":
    mcp.run(transport='stdio')
```

## Cline-MCP服务端配置

![image-20250312180624136](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250312180624136.png)

```
# Cline插件配置
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "D:\\mcp_server_demo",
        "run",
        "weather.py"
      ],
      "disabled": false
    }
  }
}
```



## 效果

![image-20250312180716085](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250312180716085.png)