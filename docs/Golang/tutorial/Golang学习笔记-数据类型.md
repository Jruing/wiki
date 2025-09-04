
[toc]

## 整型

> 整型分为两类：`有符号整型` 和 `无符号整型`
>
> 在内存中由两部分表示: `{符号位}{数字位置}`

### 有符号整型

| 类型  | 长度（字节数）               | 值的范围                                     |
| ----- | ---------------------------- | -------------------------------------------- |
| int   | 在32位平台为4，在64位平台为8 | 在32位平台等同于int32，在64位平台等同于int64 |
| int8  | 1                            | -128 ~127                                    |
| int16 | 2                            | -32768~32767                                 |
| int32 | 4                            | -2147483648~2147483647                       |
| int64 | 8                            | -9223372036854775808~9223372036854775807     |

### 无符号整型

| 类型   | 长度（字节数）               | 值的范围                                       |
| ------ | ---------------------------- | ---------------------------------------------- |
| uint   | 在32位平台为4，在64位平台为8 | 在32位平台等同于uint32，在64位平台等同于uint64 |
| uint8  | 1                            | 0~255 (2^8-1)                                  |
| uint16 | 2                            | 0~65535 (2^16-1)                               |
| uint32 | 4                            | 0~4294967295 (2^32-1)                          |
| uint64 | 8                            | 0~18446744073709551615 (2^64-1)                |

> 注意：不同类型的整型无法互相赋值，需要做类型转换。其中位数长的类型转换为位数短的类型，或者无符号的类型转换为有符号的类型时，会丢失准确性

###  栗子

```go
var age uint8 
age = 18

var money int
money = -1000
```

## 浮点型

> 浮点型表示带有小数位的数字，也叫浮点数
>
> 在内存中由三部分表示：`{符号位}{指数位}{有效数字位}`
>
> `符号位`用于表示浮点数的正负性，它占据了浮点数的最高位。0 表示正数，1 表示负数
>
> `指数位`用于表示浮点数的数量级，它通常是一个带符号的整数。指数部分的长度和浮点数的类型有关，通常为 8 位或 11 位。指数部分的值可以为正数、负数或零。
>
> `有效数字位`用于表示浮点数的精度。它通常是一个带符号的小数，长度也与浮点数的类型有关。尾数部分的值通常是一个小数，可以是正数、负数或零。

| 类型    | 长度（字节数） | 指数位(bit) | 有效数字位(bit) |
| ------- | -------------- | ----------- | --------------- |
| float32 | 4              | 8           | 23              |
| float64 | 8              | 11          | 52              |

### 栗子

```
var speed float32
speed = 35.75
height := 1.78
```

> 注意：
>
> 1. 在不声明浮点数类型的情况下，默认会识别为float64类型
> 2. 浮点型不是绝对精确的数值类型，存在一定的误差，因此在进行浮点数的比较时，需要指定精度

## 布尔型

> 布尔类型有两个值: `true` 和 `false`，只占用一个bit的大小，通常用于条件判断

### 栗子

```go
var answer bool
answer = true
```

## 字符型

> 字符型有两种：`byte` 和 `rune`，使用两个英文单引号表示`''`



| 类型 | 长度 | 编码    |
| ---- | ---- | ------- |
| byte | 1    | UTF-8   |
| rune | 4    | Unicode |

### 栗子

```
var name rune = ’jruing‘
var name byte = 'jruing'
```

## 字符串型

> 字符串类型关键字`string`，使用符号`""`表示字符串字面常量

### 栗子

```go
var name string
name = "Jruing"
```



> 注意
>
> 1. 字符串类型无法修改字符串中的某一位字符，只能重新赋值
>
> 2. 字符串默认编码为UTF-8
>
> 3. 如果需要改变字符串中的某一位字符，需要先将字符串先转换为`[]byte`或`[]rune`，改变数组中对应下标的元素，再转换为一个新的字符串
>
>  ```go
>    package main
>    
>    import (
>        "fmt"
>    )
>    
>    func main() {
>        // 定义字符串s1
>        var s1 = "hello 你好"
>        // 将字符串s1格式转换为[]byte,赋值给s2
>        var s2 = []byte(s1)
>        // 将字符串s1格式转换为[]rune,赋值给s3
>        var s3 = []rune(s1)
>    
>        // 修改s1中下标0的值
>        s2[0] = 'k'
>        // 修改s2中下标6的值
>        s3[6] = '我'
>        
>        // 将s2转换为新的字符串输出
>        fmt.Println(string(s2))
>        // 将s3转换为新的字符串输出
>        fmt.Println(string(s3))
>    }
>  ```
>

### 字符串<-->其他类型转换

```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	var v1 bool
	// 将字符串转换为布尔型
	v1, _ = strconv.ParseBool("true")
	fmt.Println(v1)

	var v2 float64
	// 将字符串转换为浮点型，第二位参数为浮点型数的位数
	v2, _ = strconv.ParseFloat("2131.393", 64)
	fmt.Println(v2)

	var v3 int64
	// 将字符串换算为整型，第二位参数表示以多少位进制进行换算，第三位为换算后的数值位数
	v3, _ = strconv.ParseInt("-116", 10, 64)
	fmt.Println(v3)

	var v4 uint64
	// 将字符串换算为无符号整型，第二位参数表示以多少位进制进行换算，第三位为换算后的数值位数
	v4, _ = strconv.ParseUint("23", 10, 64)
	fmt.Println(v4)

	var v5 string
	// 将布尔型转换为字符串
	v5 = strconv.FormatBool(false)
	fmt.Println(v5)

	var v6 string
	// 将浮点型转换为字符串，第二位参数表示输出格式，'f'为普通显示方式，取小数点后的位数做为精确位数，'e'与'E'为指数形式，'g'与'G'以有效数字位数做为精确位数，第三位表示数值精确位数，第四位表示数值所占空间位数
	v6 = strconv.FormatFloat(3.141592679, 'f', 6, 64)
	fmt.Println(v6)

	var v7 string
	// 将布尔型转换为整型
	v7 = strconv.FormatInt(-667434, 10)
	fmt.Println(v7)

	var v8 string
	// 将布尔型转换为整型
	v8 = strconv.FormatUint(32434, 10)
	fmt.Println(v8)
    
    var v9 int
	// 将字符串"2"转换为整型
	v9, _ = strconv.Atoi("2")
	fmt.Println(v9)

	var v10 string
	// 将整型值3转换为字符串
	v10 = strconv.Itoa(3)
	fmt.Println(v10)
}
```

## 数组

> 数组表示的是同一种数据类型的集合,数组中的每一个元素称为数组元素，每个元素都有对应的下标地址，从0开始，在定义数组时需要指定数组的长度，数组长度必须是整型常量
>
> 缺点：
>
> 1. 数组元素长度固定，不支持元素的删除和新增
> 2. 数组进行参数传递时采用值传递，需要进行完整赋值
>
> 语法：
>
> var {变量名} [数组长度]{数组元素类型}

### 栗子

```go
// 定义一个普通的一维数组
var name [3]string // ["jruing","hello","world"]
// 定义一个多维数组
var name [3][2]string // [["h","e"],["l","l"],["o","w"]]

// 初始化一个数组
var name [3]string = [3]string{"jruing","hello","world"}
// 初始化指定下标的数组
var name [3]string = [3]string{0:"jruing",2:"hello",1:"world"}

// 获取数组的长度 len()
length:= len(name)
```

## 切片

> 切片可以理解为数组切割出来的一部分，它不需要指定数组的大小，在不对切片进行赋值的情况下默认值为nil，切片主要用于弥补数组的不足
>
> 语法：
>
> var {变量名} [] {参数元素类型}

### 创建切片

```go
// 定义一个切片
var name []string
// 通过内置方法make定义切片,make()的第一个参数表示切片类型，第二个参数表示切片中元素的长度，第三个参数表示切片可以分配的空间大小，可以忽略第三个参数，当第三个参数在不指定的情况下切片可分配的空间大小等于初始大小
name := make([]string,5,10)
// 获取切片存储空间大小
fmt.Println(cap(name))
```

### 通过数组的方式创建切片

```go
var name [3]string = [3]string{"jruing","hello","world"}
var name2 []string
name2 = name[1:3] // 获取数组name中的 hello和world
```

### 读取/修改切片元素

```go
var name []string = []string{"jruing","hello","world"}
fmt.Println(name[0]) // 获取下标为0的元素：jruing
name[1] = "zhangsan" // 将下标为1的元素（hello）修改为zhangsan
```

### 追加元素-append

```go
var name []string = []string{"jruing","hello","world","zhangsan","lisi"}
// 将元素追加到切片最后的位置
name = append(name,"lisi","wangwu")
// 在指定位置插入元素(将插入位置后半部的切片先临时保存，再为前半部的切片追加要插入的元素，最后追加临时保存的后半部切片)
tmp := append([]string,name[2:])
name = append(name[:2],"插入的元素")
name = append(name,tmp)
```

### 合并多个切片

```go
var name1 []string = []string{"jruing","hello","world"}
var name2 []string = []string{"lisi","wangwu","zhaoliu"}
name1 = append(name1,name2)
```

### 删除元素

```go
var name []string = []string{"jruing","hello","world","zhangsan","lisi"}
// 删除world
tmp := append(name[:2],name[3:])
```

## 字典

> 字典是以键值对组成的数据，关键字为`map`, 在未赋值的情况下
>
> 语法：
>
> var 变量名 map[键的类型]值的类型

### 栗子

```go
// 定义字典 key和值为string类型
var userinfo map[string]string
// 初始化字典
userinfo = make(map[string]string)
```

### 字典读、写、删除

```go
// 定义字典
var userinfo map[string]string
// 初始化字典
userinfo = make(map[string]string)
// 赋值
userinfo['name'] = 'jruing'
// 获取指定key的值
fmt.Println(userinfo['name'])
// 获取字典长度
fmt.Println(len(userinfo))
// 删除字典中的某个key
delete(userinfo,'name')
```

## 指针

> 指针是对于变量的间接引用，其中存放了变量的内存地址。指针通过寻址可对原有的变量进行访问和修改，主要应用在以下几个场景中
>
> 1. 作为方法传参参数，指向占内存空间大的变量，以节约方法传参过程中的内存开销
> 2. 作为方法传参参数，指向需要在方法体内发生值变动后，在方法体外的值也同时需要发生变动的变量；
> 3. 定义结构体指针方法，通过引用传递实现在方法体中修改源结构体中的字段值；
> 4. 用于反射，获取所指向的元素类型。
>
> 指针有两个关键字 `&` 和 `*`
>
> `*` :  用于定义指针及获取指针的值
>
> `&` :  用于获取元素的指针地址
>
> 语法：
>
> var 指针名称 *指针指向的类型

### 栗子

```go
//  定义一个指针
var p *int

// 给指针赋值(获取变量name的变量地址并给指针赋值)
var name string
name = "jruing"
p = &name

// 通过指针修改这个指针所指向的变量的值
*p = "张三"
```

## 方法

> 方法是对一段逻辑的封装，关键字为 `func`
>
> 语法：
>
> func 方法名(入参)返回值{
>
> ​	方法体 // 具体的逻辑
>
> }

### 栗子

```go
// 求长方形的面积（长度*宽度）
func area(lengths int,width int) area_sum int {
    area_sum = lengths * width
    return 
}
// 调用函数
area(2,4)
```

## 结构体

> 结构体是一种自定义类型，是实现面向对象编程的基础，我们可以通过结构体去描述一个事物所具有的各项特性，形成对于对象的描述
>
> 语法：
>
> type 结构体名称 struct{
>
> ​	字段名 字段类型 // 字段名首字母大写才可以被结构体外部访问，小写则无法被结构体外部访问
>
> }

```go
// 定义一个用户信息的结构体
type UsesrInfo struct{
    Name string
    Age int8
    weight float32 // 该字段
}

// 初始化上面的结构体
var userinfo = UserInfo{
    Name "Jruing"
    Age 18
    weight 100.1
}

// 修改结构体中的值
userinfo.Name = "张三"


// 获取结构体中某个字段的值
fmt.Println(userinfo.Name)

// 通过结构体方法访问私有字段
func (u UserInfo) Introduce(){
    fmt.Println(p.weight)
}
```

### 结构体继承

```go
// 定义一个UserInfo的结构体
type UserInfo struct {
  	Name string
}
// 为结构体Userinfo定义方法
func (u UserInfo) Say() {
    fmt.Println("this is a function")
}
// 定义一个新的结构体User，继承UserInfo
type User struct {
    UserInfo
}

var u1 UserInfo
var u2 User
// 直接调用UserInfo的Say方法
u1.Say()
// 通过语法糖调用User所继承的UserInfo的方法Say
u2.Say()
// 显示调用继承UserInfo的方法
u2.UserInfo.Say()

```

## 接口

> 定义接口的关键字 `interface`, 不赋值的情况下默认值为 nil
>
> 空接口语法：
>
> var 接口名称 interface{
>
> }
>
> 类型接口语法:
>
> type 类型名称 interface {
>
> ​	方法名称(入参)返回值
>
> }

### 栗子

```go
package main

import (
	"fmt"
)

// 定义一个Runner接口，其中包含Run()方法
type Runner interface {
	Run()
}

// 定义一个Swimmer接口，其中包含Swim()方法
type Swimmer interface {
	Swim
}

// 定义一个Cat类型
type Cat struct{}

// Cat类型实现了Run方法，说明猫是Runner
func (c Cat) Run() {
	fmt.Println("cat can run.")
}

// 定义一个Dog类型
type Dog struct{}

// Dog类型实现了Run方法，说明狗是Runner
func (d Dog) Run() {
	fmt.Println("dog can run.")
}

// Dog类型实现了Swim方法，说明狗是Swimmer
func (d Dog) Swim() {
	fmt.Println("dog can swim.")
}

func main() {
	// 定义一个Runner接口变量runner，默认值nil
	var runner Runner
	// 定义一个Swimmer接口变量swimmer，默认值nil
	var swimmer Swimmer

	// 实例化一个Cat类型变量cat
	var cat Cat
	// 实例化一个Dog类型变量dog
	var dog Dog

	// 将cat赋值给接口runner
	runner = cat
	// 通过runner执行cat的Run()方法
	runner.Run()

	// 将dog赋值给接口runner
	runner = dog
	// 通过runner执行dog的Run()方法
	runner.Run()

	// 将dog赋值给接口swimmer
	swimmer = dog
	// 通过swimmer执行dog的Swim()方法
	swimmer.Swim()
}
```

### 类型推断

> 将接口类型变量转换成其它类型需要使用类型推断

```go
// 定义一个空接口
var name interface{}
// 方式一(若推断类型不正确，则会抛出panic异常)
{{ 推断后的变量 }} := {{ 接口变量 }}.({{ 推断类型 }})
name = "Jruing"
var st string
st = name.(string)

// 方式二
{{ 推断后的变量 }}, {{ 是否推断成功 }} := {{ 接口变量 }}.({{ 推断类型 }})
var st2 string
st2, ok := name.(string)
if !ok {
    panic("not a string type")
}
// 方式三（参数类型不确定的情况推荐使用）
switch {{ 推断后的变量 }}:={{ 接口变量 }}.(type){
case {{ 推断类型1 }}:
    ...
case {{ 推断类型2 }}:
    ...
default:
    ...
}

var st3 string
switch s:=name.(type){
    case string:
    	st3 = s
    default:
    	panic("not a string type")
}
```

