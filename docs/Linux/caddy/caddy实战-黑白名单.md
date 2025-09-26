## Caddyfile文件
```
localhost:8002 {

    # 白名单ip列表
    @allowed {
        remote_ip 192.168.1.123
		remote_ip ::1
    }
    
    # 白名单访问
    handle @allowed {
        respond "Welcome, allowed IP" 200
    }
    
    # 默认处理
    handle {
        respond "Forbidden" 403
    }
}
```