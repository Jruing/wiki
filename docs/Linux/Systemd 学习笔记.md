> Unit 的配置文件
>
> * `[Unit]`区块通常是配置文件的第一个区块，用来定义 Unit 的元数据，以及配置与其他 Unit 的关系
> * `[Install]`通常是配置文件的最后一个区块，用来定义如何启动，以及是否开机启动
> * `[Service]`区块用来 Service 的配置，只有 Service 类型的 Unit 才有这个区块

## Unit文件

```
[Unit]
# *描述
Description=Flask project
# 项目文档
# Documentation=/home/python_env/code/flask_demo1/README.md
# 项目启动时需要依赖的前置服务
# Before=network.target
# *项目启动后需要依赖的后置服务
After=network.target
# 项目启动时依赖的其他服务
# Requires: mysql.target

[Service]
# *启动方式，默认为simple，其他启动方式有forking、oneshot、notify、dbus、exec、idle
Type = forking
# 启动前执行
ExecStartPre =/bin/echo "flask_demo1 开始启动"
# *启动项目
ExecStart=/home/python_env/venv/flask_demo/bin/python flask_demo1.py
# 项目启动后执行
ExecStartPost =/bin/echo "flask_demo1 启动完成"
# 项目停止时执行
ExecStop=/bin/echo "flask_demo1 停止"
# *启动失败后重启(always:总是重启，on-success、on-failure、on-abnormal、on-abort、on-watchdog)
Restart=always
# *设置服务工作目录
WorkingDirectory=/home/python_env/code
# 指定环境变量
# Environment=FLASK_APP=flask_demo1.py
# 设置项目启动的用户
User=python_env
# 设置项目启动的用户组
Group=python_env
# 设置项目输出
# StandardOutput=syslog

[Install]
# 该参数表示此Unit是开机启动时候关联到multi-user.target
# 当multi-user.target下面的任意一个Unit启动都会触发本Unit的启动
# 即enable状态的时候会创建一个链接到/etc/systemd/system/multi-user.target.wants/目录下面
WantedBy=multi-user.target
```

> 将上述内容写入`flask_demo1.service`,将该文件放入`/usr/lib/systemd/system/`目录下,执行以下命令`systemctl daemon-reload`,然后执行`systemctl start flask_demo1.service`即可启动服务

## 常用systemctl命令

### 启动服务

systemctl start flask_demo1.service

### 停止服务

systemctl stop flask_demo1.service

### 重启服务

systemctl restart flask_demo1.service

### 查看服务状态

systemctl status flask_demo1.service

### 查看服务日志

journalctl -u flask_demo1.service

### 重载而不重启(用于重新加载 systemd 的守护进程配置,在修改service文件后需要执行)

systemctl daemon-reload

### 重载而不重启(用于重新加载服务的配置)

systemctl reload flask_demo1.service

###  普通用户执行(需要注意的是centos7执行失败，可能是systemd版本的问题)

> 需要先在普通用户的模式下创建目录`~/.config/systemd/user/`

systemctl --user start flask_demo1.service
