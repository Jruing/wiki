# CGO是什么

```
cgo 是在 Android 和 iOS 上运行 Go 程序的关键,它允许GO程序与C语言库相互操作
未用到CGO的时候，建议编译的时候禁用CGO,比如编译ARM架构的时候就需要打开该选项，该选项默认情况下为1
```

# 编译为exe可执行文件

```
go env -w CGO_ENABLED=0 # 禁用CGO
go env -w GOOS=windows # 目标平台是Windows
go env -w GOARCH=amd64 # 目标处理器架构是amd64
```

# 编译为Linux可执行文件

```
go env -w CGO_ENABLED=0 # 禁用CGO
go env -w GOOS=linux # 目标平台是Linux
go env -w GOARCH=amd64 # 目标处理器架构是amd64
```

# 编译为Mac平台64位可执行文件

```
go env -w CGO_ENABLED=0 # 禁用CGO
go env -w GOOS=darwin # 目标平台是MacOS
go env -w GOARCH=amd64 # 目标处理器架构是amd64
```

# GOARCH 中 386 与 amd64 的区别

```
386 代表 32 位系统，也称为 i386。名字源于 Intel 80386 指令集。
amd64 代表 64 位系统。名字源于 64 位指令集最早由 AMD 公司发布。
```

# 编译命令

```
go build main.go
```

注意：编译为linux可执行文件，上传到服务器后需要手动加入可执行权限 `chmod +x main`
