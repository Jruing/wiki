## 什么是跨域
> 之所以产生跨域是因为违反了同源策略，同源策略是指(相同协议:相同域名/ip:相同端口),只要有一项不一致就会产生跨域
```
# 以下两个url是违反了同源策略中的协议一致
http://www.baidu.com:8080
ftp://www.baidu.com：8080
# 以下两个url是违反了同源策略中的域名/ip一致
http://www.baidu.com:8080
http://www.google.com：8080
# 以下两个url是违反了同源策略中的端口一致
http://www.baidu.com:8080
http://www.baidu.com：8081
```
## 如何解决跨域

