# Cobra CLI 学习笔记

## 简介

> Cobra 是 Go 的 CLI 框架。它包含一个用于创建强大的现代 CLI 应用程序的库，以及一个用于快速生成基于 Cobra 的应用程序和命令文件的工具。
>
> 官方文档: https://cobra.dev/

## 安装

> ```
> go get -u github.com/spf13/cobra/cobra
> ```

## Cobra 常用参数解析

```
var rootCmd = &cobra.Command{
	Use:     "",  // 命令
	Aliases: nil, // 别名
	Short:   "",  // 对于该命令简单的介绍
	Long:    "",  // 对于该命令详细的介绍
	Example: "",  // 该命令的使用示例
	Args:    nil, // 位置参数验证
	Version: "",  // 该CLI的版本号
	PreRun:  nil, // 在Run函数执行前执行的操作
	Run:     nil, // 具体执行操作
	PostRun: nil, // 再Run函数执行后执行的操作
}
```

## 参数验证

> 位置参数：Args有以下几种验证方法
>
> - `NoArgs`- 不允许有位置参数，如果存在位置参数，该命令将提示错误。
> - `ArbitraryArgs`- 该命令将接受任何 args。
> - `OnlyValidArgs`- 如果存在任何不在 字段中的位置参数，该命令将报告错误。`ValidArgs``Command`
> - `MinimumNArgs(int)`- 指定位置参数的最小数量，如果没有至少 N 个位置参数，该命令将提示错误。
> - `MaximumNArgs(int)`-指定位置参数的最大数量， 如果位置参数超过 N个，该命令将提示错误。
> - `ExactArgs(int)`- 指定解析位置参数的数量，如果没有恰好 N 个位置参数，该命令将提示错误。
> -  `ExactValidArgs(int)`- 如果没有恰好 N 个位置参数，或者有任何位置参数不在 字段中，则该命令将报告并出错`ValidArgs``Command`
> - `RangeArgs(min, max)`- 填写一个数值，且该数值介于 最小数量和最大数量之间，否则该命令将提示错误。

## 例子

```
package main

import (
	"fmt"
	"github.com/spf13/cobra"
)

var config string
var output string

// 初始化根命令
var rootCmd = &cobra.Command{
	Use:   "tools",
	Short: "这是一个简单的描述",
	Long:  "这是一个详细的描述",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("这是一个Cobra示例", config)
	},
}

// 创建一个命令echo
var echoCmd = &cobra.Command{
	Use:   "echo",
	Short: "输出当前服务信息",
	Args:  cobra.NoArgs,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("当前服务地址：http://127.0.0.0:8000")
	}}

// 创建有一个带位置参数的命令init
var initCmd = &cobra.Command{
	Use:   "init <name>",
	Short: "初始化一个指定服务的配置",
	Args:  cobra.ExactArgs(1), // 解析位置参数name
	Run: func(cmd *cobra.Command, args []string) {
		name := args[0] // 获取位置参数name的值
		fmt.Println("开始执行初始化", name)
	},
}

// 创建命令server
var serverCmd = &cobra.Command{
	Use:   "server",
	Short: "获取服务列表",
}

// 创建命令ls，用于获取服务列表明细
var serverListCmd = &cobra.Command{
	Use:   "ls",
	Short: "获取服务列表",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("当前服务列表：\naa\nbb\ncc")
		fmt.Println("将文件输出到", output)
	},
}

// 创建带有位置参数的命令get，用于获取具体服务的信息
var serverGetCmd = &cobra.Command{
	Use:   "get <name>",
	Short: "获取具体服务信息",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		servername := args[0]
		fmt.Println("获取服务信息：", servername)
	},
}

// 运行初始化配置函数
func initConfig() {
	fmt.Println("运行初始化")
}
func main() {
	// 加载初始化配置
	cobra.OnInitialize(initConfig)

	// 将echo，init，server这三个命令加入到根命令下
	rootCmd.AddCommand(echoCmd)
	rootCmd.AddCommand(initCmd)
	rootCmd.AddCommand(serverCmd)

	// 将serverListCmd serverGetCmd 这两个命令作为子命令加入到server命令下
	serverCmd.AddCommand(serverListCmd)
	serverCmd.AddCommand(serverGetCmd)

	// Persistent Flags，持久化的flag，全局可以使用，可以给任一命令添加选项
	rootCmd.PersistentFlags().StringVar(&config, "config", "", "config file (default is $HOME/.firstappname.yaml)")

	// Flags 局部使用，为某一个命令添加选项
	serverListCmd.Flags().StringVar(&output, "output", "", "输出文件")
	serverGetCmd.Flags().StringVar(&output, "output", "", "输出文件")
	// 把 output 设置为必选项
	err := serverListCmd.MarkFlagRequired("output")
	if err != nil {
		return
	}
	// 运行
	if err := rootCmd.Execute(); err != nil {
		return
	}
}

```

## 编译打包

```
go build -o main.exe main.go
```

## 测试

```
D:\code_Go\cli_demo>main.exe -h
这是一个详细的描述

Usage:             
  tools [flags]    
  tools [command]  
                   
Available Commands:
  completion  Generate the autocompletion script for the specified shell
  echo        输出当前服务信息
  help        Help about any command
  init        初始化一个指定服务的配置
  server      获取服务列表

Flags:
      --config string   config file (default is $HOME/.firstappname.yaml)
  -h, --help            help for tools

Use "tools [command] --help" for more information about a command.

D:\code_Go\cli_demo>main.exe echo 
运行初始化
当前服务地址：http://127.0.0.0:8000

D:\code_Go\cli_demo>main.exe init aaaa
运行初始化
开始执行初始化 aaaa

D:\code_Go\cli_demo>main.exe server ls --output=111
运行初始化
当前服务列表：
aa
bb
cc
将文件输出到 111

```

