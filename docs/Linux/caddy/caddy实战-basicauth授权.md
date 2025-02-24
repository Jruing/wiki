# BasicAuth 认证

## hash-password生成密码
```
caddy hash-password
  [--plaintext <password>]
  [--algorithm <name>]
  [--salt <string>]

散列密码并以 base64 编码将输出写入标准输出，然后退出。

--plaintext是密码的明文形式。如果省略，将采用交互模式，并提示用户手动输入密码。

--algorithm可能是 bcrypt 或 scrypt。默认为 bcrypt。

--salt仅在算法需要外部盐（如 scrypt）时使用。
```
## Caddyfile
```
http://localhost {
    redir /* https://{host}{uri} permanent # 强制将http通过301重定向到https
}

https://localhost {
    # /page2 页面需要密码才能访问
    basicauth /page2 {
        # 用户名为admin,密码为test1234
        admin $2a$14$lV0e45BhVJfrXaruvFbZXu3GQjofewlENg4YmkBJUXL.2S1NWQlQC
    }
    
    # 匹配/
    handle / {
        respond "hello world" # 硬编码返回
    }

    # 匹配/page1
    handle /page1 {  
        root * www # 指定根目录
        file_server # 默认开启文件服务
    }

    # 匹配/page2
    handle /page2 { 
        respond "this is page2" 
    }
    
    # 默认处理（如果前面的路由都没有匹配）
    handle {  
        respond "错误页面"
    }
}
```
## 启动
```
caddy run --config Caddyfile
```