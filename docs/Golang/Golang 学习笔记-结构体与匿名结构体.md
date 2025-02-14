# Golang 学习笔记-结构体与匿名结构体

> 结构体：是由一系列具有相同类型或不同类型的数据构成的数据集合
>
> 匿名结构体：没有命名的结构体，其他与普通结构体一致，匿名结构体一般用于函数内部
>
> 匿名字段：是指结构体内部没有命名的字段，局限性强，一个结构体内部不能定义两个相同数据类型的匿名字段

## 栗子

```
package main

import "fmt"

// 定义结构体
type NormalStruct struct {
	name string
	age  int8
}

func LambdaStruct() {
	// 结构体
	n := NormalStruct{
		name: "张三",
		age:  0,
	}
	fmt.Println("结构体", n.name)
	// 匿名结构体(只能在函数内部调用，适合一次性)
	lambdaStruct := struct {
		name string
	}{
		name: "Jruing",
	}
	fmt.Println("匿名结构体", lambdaStruct.name)
	// 匿名字段(局限性强，同一种类型只能写一个)
	lambdaField := struct {
		string
		int8
	}{"李四", 18}
	fmt.Printf("匿名字段：姓名：%v,年龄：%v", lambdaField.string, lambdaField.int8)
}

func main() {
	LambdaStruct()
}
```

