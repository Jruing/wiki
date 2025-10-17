> goto 是一个跳转语句，可以让程序直接跳转到当前函数内某个标记（label）处继续执行。
> 注意：goto 语句只能跳转到当前函数内的某个标记，不能跳转到其他函数的某个标记，且goto跳转后，不会再回去执行它后面的代码
## 例子
```
package main

import (
	"fmt"
	"math/rand"
)

func main() {
	fmt.Println("hello")
	randNum := rand.Intn(20)
	fmt.Println("当前随机数字", randNum)
	if randNum >= 10 {
		// 跳转到End标签
		goto End
	} else {
		fmt.Println("world")
	}
// 声明标签
End:
	fmt.Println("End")
}
```

## 结果
```
PS C:\workspace\yuanread> go run .\test.go
hello
当前随机数字 3
world
End

PS C:\workspace\yuanread> go run .\test.go
hello
当前随机数字 12
End
PS C:\workspace\yuanread> 
```