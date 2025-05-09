# MCP学习笔记-查询主机资源使用情况

## 环境准备

- CherryStudio

- Python

## monitor.py

```
import paramiko
import time

class LinuxMonitor:
    def __init__(self, hostname, username, password, port=22):
        """初始化SSH连接参数"""
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.client = None

    def connect(self):
        """建立SSH连接"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
                port=self.port
            )
            print(f"Successfully connected to {self.hostname}")
            return True
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            return False

    def disconnect(self):
        """关闭SSH连接"""
        if self.client:
            self.client.close()
            print("Connection closed")

    def execute_command(self, command):
        """执行Shell命令并返回结果"""
        if not self.client:
            print("Not connected to host")
            return None
        
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode('utf-8').strip()

    def get_cpu_usage(self):
        """获取CPU使用率"""
        command = "top -bn1 | grep 'Cpu(s)' | awk '{print $2}'"
        result = self.execute_command(command)
        return float(result) if result else 0

    def get_memory_usage(self):
        """获取内存使用情况"""
        command = "free | grep Mem | awk '{print $3/$2 * 100.0}'"
        result = self.execute_command(command)
        return float(result) if result else 0

    def get_disk_usage(self):
        """获取磁盘使用情况"""
        command = "df -h / | tail -1 | awk '{print $5}' | cut -d'%' -f1"
        result = self.execute_command(command)
        return float(result) if result else 0

    def get_io_usage(self):
        """获取IO使用情况"""
        command = "iostat -c 1 1 | tail -2 | head -1 | awk '{print $1}'"
        result = self.execute_command(command)
        return float(result) if result else 0

    def get_all_metrics(self):
        """获取所有指标"""
        metrics = {
            'cpu_usage': self.get_cpu_usage(),
            'memory_usage': self.get_memory_usage(),
            'disk_usage': self.get_disk_usage(),
            'io_usage': self.get_io_usage()
        }
        return metrics
```

## main.py

```
# encoding: utf-8
from mcp.server.fastmcp import FastMCP
from monitor import LinuxMonitor
# 创建一个FastMCP服务
mcp = FastMCP("host", "获取主机资源使用情况")

@mcp.prompt("获取主机资源使用率",description="获取主机资源使用率")
async def prompt(hostname:str,username:str,password:str) -> str:
    """Prompt for a string"""
    monitor = LinuxMonitor(
        hostname=hostname,
        username=username,
        password=password
    )
    try:
        if monitor.connect():
            # 获取并打印所有指标
            metrics = monitor.get_all_metrics()
            return f"""\n主机IP：{hostname}\n系统指标:
            CPU 使用率: {metrics['cpu_usage']:.2f}%
            内存使用率: {metrics['memory_usage']:.2f}%
            磁盘使用率: {metrics['disk_usage']:.2f}%
            IO 使用率: {metrics['io_usage']:.2f}%
            """
    finally:
        monitor.disconnect()

if __name__ == "__main__":
    mcp.run("sse")
```

## 效果

![image-20250509103240259](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250509103240259.png)

![image-20250509103315917](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250509103315917.png)