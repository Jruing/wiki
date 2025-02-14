# Golang学习笔记-定时任务

## 指定具体时间执行

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	// 指定执行时间为 2023-11-29 00:00:00
	executionTime := time.Date(2023, time.November, 29, 0, 0, 0, 0, time.UTC)

	// 当前时间
	now := time.Now().UTC()

	// 计算距离执行时间的持续时间
	duration := executionTime.Sub(now)

	// 使用 time.AfterFunc 安排在指定时间执行的函数
	time.AfterFunc(duration, func() {
		fmt.Println("执行定时任务...")
		// 在这里添加你的任务逻辑
	})

	// 主程序可以继续执行其他工作
	// ...

	// 阻塞程序，直到按下 Ctrl+C 才退出
	select {}
}

```

## 定期执行

### 1. time模块

```
package main

import (
	"fmt"
	"time"
)

func main() {
	// 创建一个定时器，每隔一段时间触发一次
	ticker := time.NewTicker(5 * time.Second)

	// 启动一个 goroutine 来处理定时任务
	go func() {
		for {
			select {
			case <-ticker.C:
				// 这里写入你想要定期执行的任务
				fmt.Println("定时任务执行:", time.Now())
			}
		}
	}()

	// 等待程序结束，可以使用通道或者其他方式
	select {}
}
```

### 2.cron模块

> go get github.com/robfig/cron

```
package main

import (
	"fmt"
	"github.com/robfig/cron"
)

func main() {
	// 创建一个新的 cron 实例
	c := cron.New()

	// 添加你的定时任务，这里是一个每分钟执行一次的例子
	c.AddFunc("* * * * *", func() {
		fmt.Println("执行定时任务...")
	})

	// 启动 cron
	c.Start()

	// 主程序可以继续执行其他工作
	// ...

	// 阻塞程序，直到按下 Ctrl+C 才退出
	select {}
}

```

