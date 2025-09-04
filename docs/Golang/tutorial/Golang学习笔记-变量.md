## 声明变量
> 声明变量关键字`var`
```
var {变量名称} {变量类型}
```

### 例子

```go
// 声明一个变量为v1的整型变量，未赋值时默认值为0
var v1 int
// 声明一个变量为v2的浮点型变量，未赋值时默认值为0
var v2 float32
// 声明一个变量为v3的数组变量(数组中的元素为整型)，未赋值时默认值为nil
var v3 [10]int
// 声明一个变量为v4的数组变量，未赋值时默认值为nil
var v4 []float32
// 声明一个变量为v5的数组变量
var v5 struct {
	age int
	name string
}
// 声明一个变量为v6的指针变量，未赋值时默认值为nil
var v6 *int
// 声明一个字典变量，未赋值时默认值nil
var v7 map[string]string
// 声明一个方法变量，未赋值时默认值nil
var v8 func(x int)int
// 声明一个接口变量，未赋值时默认值nil
var v9 interface{}
```

## 变量赋值

```go
// 指定变量类型且对变量赋值
var {变量名} {变量类型} = {变量值}
var age int = 18
// 根据变量值自动推断变量类型(方法一)
var {变量名} = {变量值}
var age = 18
// 根据变量值自动推断变量类型(方法二)
{变量名} := {变量值}
age := 18
```

