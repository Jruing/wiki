# 令牌桶限流

## 简介

> 令牌桶（Token Bucket）是一种常见的限流算法，用于控制请求的速率。它通过模拟一个“装满令牌的桶”来限制流量，确保系统的稳定性和公平性

## 原理

1. **令牌生成** ：
   系统以固定的速率向桶中添加令牌（例如每秒 10 个令牌）。这些令牌代表允许的请求权限。
2. **请求处理** ：
   每当有请求到达时，系统会从桶中取出一个令牌。如果桶中有足够的令牌，则请求被允许；如果没有足够的令牌，则请求被拒绝或排队等待。
3. **桶容量限制** ：
   桶的容量是有限的，多余的令牌会被丢弃。这确保了即使在低流量期间，系统也不会积累过多的令牌。
4. **速率控制** ：
   令牌的生成速率决定了系统的最大吞吐量，而桶的容量则决定了系统的突发流量能力。

## **令牌桶的工作流程**

假设我们有一个令牌桶，其配置如下：

- **令牌生成速率** ：每秒 10 个令牌。
- **桶的最大容量** ：50 个令牌。

### 正常情况

- 系统每秒生成 10 个令牌，并将它们放入桶中。
- 如果请求到达，且桶中有令牌，则消耗一个令牌并处理请求。
- 如果桶为空，则拒绝请求或让请求等待。

### 突发流量

- 如果系统在某段时间内没有收到请求，桶中的令牌会逐渐积累，最多达到桶的最大容量（50 个）。
- 当突发流量到来时，系统可以快速处理多个请求，直到桶中的令牌耗尽。

------

## **令牌桶的特点**

1. **平滑处理流量** ：
   即使请求速率波动较大，令牌桶也能平滑地处理流量，避免系统过载。
2. **支持突发流量** ：
   桶的容量允许系统在短时间内处理超过平均速率的请求。
3. **灵活性** ：
   可以通过调整令牌生成速率和桶容量来适应不同的业务需求。
4. **简单高效** ：
   实现逻辑简单，适合高并发场景。

## **令牌桶的实现示例**

```
package main

import (
    "fmt"
    "sync"
    "time"
)

type TokenBucket struct {
    rate         int64         // 令牌生成速率（每秒生成的令牌数）
    capacity     int64         // 桶的最大容量
    tokens       int64         // 当前桶中的令牌数量
    lastTime     time.Time     // 上次更新时间
    lock         sync.Mutex    // 互斥锁，保证线程安全
}

// NewTokenBucket 创建一个新的令牌桶
func NewTokenBucket(rate, capacity int64) *TokenBucket {
    return &TokenBucket{
        rate:     rate,
        capacity: capacity,
        tokens:   capacity, // 初始时桶是满的
        lastTime: time.Now(),
    }
}

// Allow 检查是否允许请求
func (tb *TokenBucket) Allow() bool {
    tb.lock.Lock()
    defer tb.lock.Unlock()

    // 计算当前应该生成的令牌数量
    now := time.Now()
    elapsed := now.Sub(tb.lastTime).Seconds()
    tb.tokens += int64(elapsed * float64(tb.rate))
    if tb.tokens > tb.capacity {
        tb.tokens = tb.capacity // 超过容量的部分丢弃
    }
    tb.lastTime = now

    // 检查是否有足够的令牌
    if tb.tokens >= 1 {
        tb.tokens--
        return true
    }
    return false
}

func main() {
    bucket := NewTokenBucket(10, 50) // 每秒生成 10 个令牌，桶容量为 50

    for i := 0; i < 60; i++ {
        if bucket.Allow() {
            fmt.Println("Request allowed")
        } else {
            fmt.Println("Request denied")
        }
        time.Sleep(100 * time.Millisecond) // 模拟每 100ms 发送一个请求
    }
}
```

## **适用场景**

1. **API 限流** ：
   控制 API 的请求速率，防止恶意请求导致系统崩溃。
2. **消息队列** ：
   控制消息的消费速率，避免消费者过载。
3. **网络流量控制** ：
   限制上传或下载的带宽。
4. **分布式系统** ：
   在分布式环境中协调多个服务的访问频率。