
## 声明常量

> 声明常量关键字: `const`

```go
const {常量名} {常量类型} 或 const {常量名} = {常量值}
```

## 预定义常量

> 预定义常量：`true` , `false` , `iota`
>
> 其中`true` , `false` 是布尔类型, `iota` 是一个自增常量，从0开始取值它每出现一次，它自身的值会加1

### iota用法

```go
const {
	money0 = iota // 值为0
    money1 = iota // 值为1
    money2 = iota // 值为2
    money3 = iota // 值为3
    money4 = iota // 值为4
    money5 = iota // 值为5
    money6 = iota // 值为6
}
```

## 常量赋值

### 例子

```go
// 定义年龄
const age int =18
// 定义姓名及年龄(方法一)
const (
	name = "jruing"
    age = 18
)
// 定义姓名及年龄(方法二)
const name,age = "jruing",18
// 定义年龄及身高
const age,height int = 18,180
```

