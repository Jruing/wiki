> 判断有两种：`if` 和 `switch`

## if判断

> `if`用于条件判断，它会按照顺序一次执行，当`if`条件及`else if`条件都不成立，则会执行`else`部分的逻辑

### 语法

```
if 条件判断 {
    ...
}else if 条件判断 {
    ...
}else {
    ...
}
```

### 栗子

```go
var money int = 18
if money >0 && money <=1000 {
    fmt.Println("有点钱")
} else if money >1000{
    fmt.Println("很有钱")
} else {
    fmt.Println("没钱")
}
```

## switch判断

> `switch` 主要用于逻辑判断，中间包含多个条件（case），执行switch判断的时候会按照case的顺序依次进行判断，当所有的判断都不成立，则会执行`default`中的逻辑,其中case中的判断条件可以是单独的一个常量，也可以是变量

### 语法
```
switch {
case 条件判断1:
    ...
case 条件判断2:
    ...
default:
    ...
}
```

### 栗子

```
var score int = 61
switch  {
	case score < 60:
		fmt.Println("不及格")
	case score >= 60 && score <= 100:
		fmt.Println("及格了")
	default:
		fmt.Println("分数不对")
}



var light string = "red"
switch  light {
	case "red":
		fmt.Println("红灯")
	case "yellow":
		fmt.Println("黄灯")
	case "green":
		fmt.Println("绿灯")
	default:
		fmt.Println("灯坏了")
}

```

