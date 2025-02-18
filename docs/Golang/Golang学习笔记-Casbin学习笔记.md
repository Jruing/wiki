# Golang学习笔记-Casbin RBAC学习

## 简介

Casbin是一个强大且高效的开源访问控制库，支持各种访问控制模型，用于在全局范围内执行授权。

支持多种编程语言：Python、Golang、Java、Php、Rust、C++、Nodejs、.NET

参考文档：https://casbin.org/zh/docs/， Casbin权限在线编辑器：https://casbin.org/zh/editor/

**注意**：Casbin只负责控制授权，不负责用户登录校验及管理用户

## 工作原理

Casbin一般由4部分组成：`策略(Policy)`，`效果(Effect)`，`请求(Request)`和`匹配器(Matcher)`, 这四个合起来就是`PERM元模型`，不同的模型则会新增定义，我们这里用的是RBAC模型，所以还会新增一个`Role`

### Request

> 定义请求参数，它是一个元组对象，这个元组对象中包含了`主体(sub)`，`访问的资源对象(obj)` 和 `动作（资源对象的访问方法 act）`，最少需要这三个对象

定义一个Request， `r={sub,obj,act}` ,指定了访问控制匹配函数所需要的参数及参数的顺序

### Policy

> 定于策略模型，它和Request一样是一个元组对象，不过它没有`eft`参数，它制定了策略规则文档中的参数和顺序

定义一个Policy，`p={sub,obj,act,eft}`, eft可忽略，若eft未定义的话，匹配策略将默认为允许

### Matcher

> 定义请求和策略的匹配规则

定义一个Matcher，`m = r.sub == p.sub && r.act == p.act && r.obj == p.obj`, 这个匹配器代表的含义是如果请求的参数在策略中存在，则返回策略结果`eft`，eft由两种结果`allow` 和 `deny`

### Effect

> 对匹配器的返回结果进行逻辑判断

`e = some(where(p.eft == allow))` ，如果任意匹配结果为allow，则结果为真

## 实战学习

可以使用文章开头提供的在线编辑器进行测试学习

我们选择的模型为`RBAC with Domains`,所以模型配置文件如下

```
// 定义请求
[request_definition]
r = sub, dom, obj, act

// 定义策略
[policy_definition]
p = sub, dom, obj, act

// 定义角色
[role_definition]
// 这三个下划线代表下面策略中g后面的3个参数
g = _, _, _

// 定义效果
[policy_effect]
e = some(where (p.eft == allow))

// 定义匹配器
[matchers]
// 1.匹配角色 2.判断请求中的域和策略中的域是否一致 3.下来判断请求中的资源对象和策略中的资源对象是否一致 4 判断请求中的动作和策略中的动作是否一致，若每一项逻辑判断结果都为真，则最终结果是allow
m = g(r.sub, p.sub, r.dom) && r.dom == p.dom && r.obj == p.obj && r.act == p.act
```

我们使用策略如下

```
// p 代表策略
// 创建一个请求者为admin，域为domain1，请求资源为data1，动作为read的策略，其实就是允许<domain1>这个域下面<admin这个用户或者角色><读取>资源对象<data1>，这个<admin>可以是用户也可以是角色，目前在这里指的是角色
p, admin, domain1, data1, read
p, admin, domain1, data1, write
p, admin, domain2, data2, read
p, admin, domain2, data2, write
// 这里指定的是使用用户直接访问
p, bob, domain1, data1, read
// g 代表角色
// 将alice这个用户加入到domain1域下面admin这个角色中
g, alice, admin, domain1
g, bob, admin, domain2
```

模拟请求进行验证

```
// 模拟使用角色<admin>下面的用户<alice>读取<read>资源<data1>，如果第一个参数指定的是用户，他会先去策略表中角色定义列表去匹配，然后利用角色名去和策略进行对比，可以看看验证结果中的前两条结果，这两条结果是一致的
alice, domain1, data1, read
// 模拟使用角色访问资源
admin, domain1, data1, read
// 使用用户名访问，<domain1>这个域下其实是匹配不到<bob>这个用户的，但是上面的策略独立定义了一条规则，允许bob直接访问domain1下面的资源data1
bob, domain1, data2,read
// 策略里没有data3这个资源对象，所以它的匹配结果为false
bob, domain1, data3,read
```
验证结果

```
true Reason: ["admin","domain1","data1","read"]
true Reason: ["admin","domain1","data1","read"]
true Reason: ["bob","domain1","data2","read"]
false
```

