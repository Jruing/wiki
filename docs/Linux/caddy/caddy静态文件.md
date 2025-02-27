# 列出目录索引
```
# --browse 启用目录索引(目录不可以用index文件,否则则会转变为站点模式)
caddy file-server --browse --listen :9090
```

# 静态文件
```
# --listen 指定监听端口
# --root 指定静态文件目录
caddy file-server --root www/ --listen :9091
```