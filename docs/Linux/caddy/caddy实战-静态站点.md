## 准备工作
- 安装caddy
- 一个html文件
## 配置
```
http://localhost {
    redir /* https://{host}{uri} permanent # 强制将http通过301重定向到https
}

https://localhost {
    # 匹配/
    handle / {
        respond "hello world" # 硬编码返回
    }

    # 匹配/page1
    handle /page1 {  
        root * www # 指定根目录
        file_server browse # 默认开启文件服务
    }

    # 匹配/page2
    handle /page2 { 
        respond "this is page2" 
    }
    
    # 默认处理（如果前面的路由都没有匹配）
    handle {  
        respond "未找到页面"
    }
}
```

## 运行
```
caddy run --config Caddyfile
```
