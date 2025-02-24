# 安装
> 下载地址：https://github.com/caddyserver/caddy/releases
```
# 解压
tar -zxvf caddy_2.9.1_linux_amd64.tar.gz
mv caddy /usr/local/bin
```
# 验证
```
# 启动服务
caddy run
# 后台启动
caddy start
# 停止服务(当cadd服务后台启动时)
caddy stop
# 重载配置文件
caddy reload

# 新的窗口访问
curl localhost:2019/config/
```

# 一个新的配置文件Caddyfile.json
> 建议使用json格式，不建议使用自带的Caddyfile格式
```
{
	"apps": {
		"http": {
			"servers": {
				"example": {
					"listen": [":2015"],# 监听端口
					"routes": [
						{
							"handle": [{
								"handler": "static_response",
								"body": "Hello, world!" # 响应内容
							}]
						}
					]
				}
			}
		}
	}
}
```
# 更新配置
```
curl localhost:2019/load \
	-X POST \
	-H "Content-Type: application/json" \
	-d @Caddyfile.json
```
# 验证配置更新
```
curl localhost:2019/config/
```
# 访问验证
```
curl localhost:2015
```