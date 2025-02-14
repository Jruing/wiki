
[toc]



## 准备一个静态登录页面demo

> 需要将下面的两个文件`index.html`和`index.css`放到nginx安装目录下html目录中

### HTML静态页面-index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>login</title>
    <link rel="stylesheet" href="./index.css">
</head>
<body>
    <div class="login-box">
        <h2>Login</h2>
        <form action="">
            <div class="user-box">
                <input type="text" name="" required>
                <label for="">username</label>
            </div>
            <div class="user-box">
                <input type="password" name="" required>
                <label for="">password</label>
            </div>
            <a href="">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                Submit
            </a>
        </form> 
    </div>
    
</body>
</html>
```

### CSS样式文件-index.css

```css
html{
    height: 100%;
}
body{
    margin: 0;
    padding: 0;
    font-family: sans-serif;
    background: linear-gradient(#141e30, #243b55);
}
.login-box{
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 400px;
    padding: 40px;
    background: rgba(0,0,0,.6);
    box-sizing: border-box;
    box-shadow: 0 15px  25px rgba(0, 0, 0, .6);
    border-radius: 10px;
}
.login-box h2{
    margin: 0  0 30px;
    padding: 0;
    color: #fff;
    text-align: center;
}
.login-box .user-box{
    position: relative;
}
.login-box .user-box input{
    width: 100%;
    padding: 10px 0;
    font-size: 20px;
    color: #fff;
    margin-bottom: 30px;
    border: none;
    border-bottom: 1px solid #fff;
    outline: none;
    background: transparent;
}
.login-box .user-box label{
    position: absolute;
    top: 0;
    left: 0;
    padding: 10px 0;
    color: #fff;
    pointer-events: none;
    transition: .3s;
}
.login-box .user-box input:focus~label,
.login-box .user-box input:valid~label{
    top: -20px;
    left: 0;
    color: #03e9f4;
    font-size: 12px;
}
.login-box form a{
    position: relative;
    display: inline-block;
    padding: 10px 20px;
    font-size: 16px;
    color: #03e9f4;
    text-decoration: none;
    letter-spacing: 4px;
    overflow: hidden;
    transition: .5s;
    margin-top: 40px;
    text-transform: uppercase;
}
.login-box form a:hover{
    background: #03e9f4;
    color: #fff;
    border-radius: 5px;
    box-shadow: 0 0 5px #03e9f4,
       0 0 25px #03e9f4,
       0 0 50px #03e9f4,
       0 0 80px #03e9f4;
}

/* 开始动画 */

.login-box a span{
    position: absolute;
    display: block;
}

/* 第一根线 上侧 从左至右 */
.login-box a span:nth-child(1){
    top: 0;
    left: -100%;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg,transparent,#03e9f4);

    /* 动画持续1s 匀速 无限次运行 */
    animation: an-1 1.5s linear infinite;
}
@keyframes an-1 {
    0%{
        left: -100%;
    }
    50%,100%{
        left: 100%;
    }
}


/* 第二根线 右侧 从上至下 */
.login-box a span:nth-child(2){
    right: 0;
    top: -100%;
    width: 2px;
    height: 100%;
    background: linear-gradient(180deg,transparent,#03e9f4);

    /* 动画持续1s 匀速 无限次运行 */
    animation: an-2 1.5s linear infinite;
    animation-delay: .25s;
}
@keyframes an-2 {
    0%{
        top: -100%;
    }
    50%,100%{
        top: 100%;
    }
}


/* 第三根线  下侧 从右至左 */
.login-box a span:nth-child(3){
    bottom: 0;
    right: -100%;
    width: 100%;
    height: 2px;
    background: linear-gradient(270deg,transparent,#03e9f4);

    /* 动画持续1s 匀速 无限次运行 */
    animation: an-3 1.5s linear infinite;
    animation-delay: .5s;
}
@keyframes an-3 {
    0%{
        right: -100%;
    }
    50%,100%{
        right: 100%;
    }
}

/* 第四根线  左侧 从下至上 */
.login-box a span:nth-child(4){
    left: 0;
    bottom: -100%;
    width: 2px;
    height: 100%;
    background: linear-gradient(360deg,transparent,#03e9f4);

    /* 动画持续1s 匀速 无限次运行 */
    animation: an-4 1.5s linear infinite;
    animation-delay: .75s;
}
@keyframes an-4 {
    0%{
        bottom: -100%;
    }
    50%,100%{
        bottom: 100%;
    }
}
```

## Nginx配置文件-nginx.conf

```nginx
#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;
#pid        logs/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';
    #access_log  logs/access.log  main;
    sendfile        on;
    #tcp_nopush     on;
    #keepalive_timeout  0;
    keepalive_timeout  65;
    #gzip  on;
    server {
        listen       80;  # 监听的端口
        server_name  localhost; # 主机IP

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html; # 默认存放静态文件的目录
            index  index.html index.htm;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}
```

## 启动Nginx

```shell
nginx -c nginx配置文件路径 # 如果不指定配置文件路径则使用默认的配置文件
```

## 样例展示

> 浏览器访问 http://localhost:80

![image-20230704133455385](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20230704133455385.png)
