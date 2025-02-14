## 今日网站

aHR0cHM6Ly93d3cuY2NwcmVjLmNvbS9wcm9qZWN0U2VjUGFnZS8jL2NxenI=

## 抓包分析

![image-20220222155132543](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20220222155132543.png)

![image-20220222155145594](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20220222155145594.png)



## 打上断点

![image-20220222155240015](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20220222155240015.png)

刷新

![image-20220222155330204](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20220222155330204.png)

## 分析堆栈

![image-20220222155849694](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20220222155849694.png)

![image-20220222160104410](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20220222160104410.png)

加密的参数是`l` ,加密前的参数是`'{"id":"rsubtrx19v4o35b1","projectKey":"honsan_cloud_ccprec","clientKey":"rsubtrw8t68wb157","token":null,"acts":[{"id":"rsubtrwsp80cx51c","fullPath":"/ccprec.com.cn.web/client/info/cqweb_nonphy_cqzr","args":[1,20,null]}]}'`

![image-20220222160207249](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20220222160207249.png)



放开断点运行,控制台输出了解密后的结果

![image-20220222160651942](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20220222160651942.png)



加入断点

![image-20220222160952921](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20220222160952921.png)





## 启动Jsrpc后端

![image-20220222161925170](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20220222161925170.png)

## 赋值加密函数
上面图片中提到了加密函数`this.aes.encode`,打开断点,执行到该加密函数的时候赋值给 aes_func,然后放开debug

![image-20220222164340618](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20220222164340618.png)


## Jsrpc解密
控制台输入

```
function Hlclient(wsURL) {
    this.wsURL = wsURL;
    this.handlers = {};
    this.socket = {};

    if (!wsURL) {
        throw new Error('wsURL can not be empty!!')
    }
    this.connect()
}

Hlclient.prototype.connect = function () {
    console.log('begin of connect to wsURL: ' + this.wsURL);
    var _this = this;
    try {
        this.socket["ySocket"] = new WebSocket(this.wsURL);
        this.socket["ySocket"].onmessage = function (e) {
            console.log("send func", e.data);
            _this.handlerRequest(e.data);
        }
    } catch (e) {
        console.log("connection failed,reconnect after 10s");
        setTimeout(function () {
            _this.connect()
        }, 10000)
    }
    this.socket["ySocket"].onclose = function () {
        console.log("connection failed,reconnect after 10s");
        setTimeout(function () {
            _this.connect()
        }, 10000)
    }

};
Hlclient.prototype.send = function (msg) {
    this.socket["ySocket"].send(msg)
}

Hlclient.prototype.regAction = function (func_name, func) {
    if (typeof func_name !== 'string') {
        throw new Error("an func_name must be string");
    }
    if (typeof func !== 'function') {
        throw new Error("must be function");
    }
    console.log("register func_name: " + func_name);
    this.handlers[func_name] = func;

}
Hlclient.prototype.handlerRequest = function (requestJson) {
	var _this = this;
	var result=JSON.parse(requestJson);
	//console.log(result)
	if (!result['action']) {
        this.sendResult('','need request param {action}');
        return
    }
	action=result["action"]
    var theHandler = this.handlers[action];
    try {
		if (!result["param"]){
			theHandler(function (response) {
				_this.sendResult(action, response);
			})
		}else{
			theHandler(function (response) {
				_this.sendResult(action, response);
			},result["param"])
		}
		
    } catch (e) {
        console.log("error: " + e);
        _this.sendResult(action+e);
    }
}

Hlclient.prototype.sendResult = function (action, e) {
    this.send(action + atob("aGxeX14") + e);
}
```

## 创建加密的调用接口

```
var jiami = new Hlclient("ws://127.0.0.1:12080/ws?group=cc&name=changchun&action=jiami&param=yes")
```



## 编写加密接口

```
# 注册一个名称为jiami的方法
jiami.regAction("jiami", function (resolve,param) {
     var a={"id":"rstyd9hkvm8ykwhx","projectKey":"honsan_cloud_ccprec","clientKey":"rstyd9ghzxc05icg","token":null,"acts":[{"id":"rstyd9hd528bi7vw","fullPath":"/ccprec.com.cn.web/client/info/cqweb_nonphy_cqzr","args":[parseInt(param),20,null]}]}
    s = JSON.stringify(a);
    l = aes_func.encode(s)
    resolve(l);
})
```

## 测试加密接口

地址: http://127.0.0.1:12080/go?group=cc&name=changchun&action=jiami&param=1, param指的是页数

![image-20220222164602914](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20220222164602914.png)





## 创建解密接口

```
var jiemi = new Hlclient("ws://127.0.0.1:12080/ws?group=cc&name=changchun&action=jiemi&param=yes")
```



## 编写解密接口

```
jiemi.regAction("jiemi", function (resolve,param) {
    console.log(param);
    l = aes_func.decode(param)
    resolve(l);
})
```

## 测试解密接口

地址:http://127.0.0.1:12080/go?group=cc&name=changchun&action=jiami&param=,param为请求文章第一步请求接口后返回的加密结果

![image-20220222170126505](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20220222170126505.png)
