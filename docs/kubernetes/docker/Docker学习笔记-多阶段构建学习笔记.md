## 准备工作

* centos 7
* docker>=19.03
* 镜像：`golang:1.22`  ` golang:1.22-alpine`

## Golang文件

```
package main

import (
	"fmt"
	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello, World!")
}

func main() {
	http.HandleFunc("/", handler)
	if err := http.ListenAndServe(":8080", nil); err != nil {
		panic(err)
	}
}
```

## Dockerfile

```
FROM golang:1.22 as go1 # 使用golang:1.22为第一阶段的基础镜像，别名为go1
WORKDIR /app # 设定工作目录
COPY . . # 将dockerfile所在目录的文件拷贝到/app下
RUN go mod init demo&&CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main . && chmod +x main # 编译main.go文件并输出可执行文件main

FROM golang:1.22-alpine as go2 #使用golang:1.22-alpine为第二阶段的镜像，别名为go2
WORKDIR /app
COPY --from=go1 /app/main . # --from 引用第一阶段go1的最终产物`main`文件，并将该文件复制到/app目录下
EXPOSE 8080 # 对外开放8080端口
CMD [ "./main" ] # 运行main文件
```

## 构建镜像

> --platform : 指定平台
>
> -t: 指定tag

```
docker buildx build --platform linux/amd64 -t go_demo1:0.1 .
```

## 构建指定阶段镜像

> --target 某一阶段的别名

```
docker buildx build --platform linux/amd64 --target go1 -t go_demo1:0.1 .
```

## 启动容器

```
docker run -itd -p 8080:8080 go_demo1:0.1
```

