
> 密码是采用bcrypt加密

## 创建web.yml配置文件

```yaml
basic_auth_users:
	# 密码生成地址:https://www.bejson.com/encrypt/bcrpyt_encode/，格式为 [ 用户名：密码 ]
    admin: $2y$10$wUvMZwoFs4/PFTZAAysAGe.c5gSqU9.9DHinCtG3ec83e9fSeuoBi
```

## 校验配置

```shell
promtool.exe check web-config web.yml
# 出现以下内容就代表配置格式正确
# web.yml SUCCESS
```

## 重启Prometheus

```shell
prometheus.exe --config.file=prometheus.yml --web.config.file=web.yml
```
