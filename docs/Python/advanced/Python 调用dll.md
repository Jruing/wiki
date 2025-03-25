# Python 调用dll
> 为了方便python调用main.go种的Sum函数,需要先将main.go打包为dll文件,利用python调用dll文件
## GO代码
main.go
```
package main

import "C"
import "fmt"

//export PrintBye
func PrintBye() {
    fmt.Println("From DLL: Bye!")
}

//export Sum
func Sum(a int, b int) int {
    return a + b;
}

func main() {
    // Need a main function to make CGO compile package as C shared library
}
```

## 将main.go打包为dll文件(需要gcc环境,[下载地址](https://wwi.lanzous.com/iyTRVnhvtrc))
> go build -ldflags "-s -w" -buildmode=c-shared -o main.dll main.go

## python调用main.dll
```
import ctypes
dll = ctypes.WinDLL(r'D:\Go_project\src\hello\a.dll')
print(dll.Sum(1,2))
```

