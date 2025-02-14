[toc]
## Refer模块防盗

> Nginx 用于实现防盗链功能的模块为 refer 模块,其依据的原理是根据请求头中的`referer`字段判断，如果referer字段合法则可以正常访问，否则判断为盗链，禁止访问

```
none: 允许缺失 referer 头部的请求访问
blocked: 有 referer 这个字段，但是其值被防火墙或者是代理给删除了
server_names: 若 referer 中的站点域名和 server_names 中的某个域名匹配，则允许访问任意字符或者正则表达式
```
## 缺点
> 由于是根据浏览器请求头中的`referer`字段进行判断的，但是这个字段是可以被模拟或者篡改的，在安全性及实用性上并不是很高
## 如何篡改或模拟请求头中的refere字段
```
import requests
header = {
"referer":"http://wwww.baidu.com"
}
response = requests.get("https://www.baidu.com",headers=header)
```

