# Golang 学习笔记-context上下文管理器

context.WithValue

> 通过`context.WithValue` 传值

```
func Ctx_demo(ctx context.Context) {
	fmt.Println("获取上下文的参数")
	name := ctx.Value("name")
	fmt.Println(name)
}

func main() {
	ctx := context.Background()
	ctx = context.WithValue(ctx, "name", "张三")
	Ctx_demo(ctx)
}
```

