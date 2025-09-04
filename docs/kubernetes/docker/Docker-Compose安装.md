# Docker-Compose安装

## 下载

> https://github.com/docker/compose/releases

## 安装

> 将文件上传到 /usr/local/src路径下

```
# 赋予可执行权限
chmod +x /usr/local/src/docker-compose
# 查看版本
[root@localhost ~]# docker-compose -v
Docker Compose version v2.24.0-birthday.10

```

## 配置文件参数
```
version: '3.8'  # 推荐使用 3.x 版本，支持大部分新特性
services:
  # 服务名（自定义，如 web、db）
  web:
    image: nginx:alpine  # 使用的镜像
    build: ./app         # 若需构建镜像，指定 Dockerfile 所在目录
    container_name: my-web  # 容器名称（默认：项目名_服务名_序号）
    restart: always      # 重启策略（always/on-failure/no）
    ports:               # 端口映射（宿主机:容器）
      - "8080:80"
      - "443:443"
    volumes:             # 数据卷挂载
      - ./html:/usr/share/nginx/html  # 宿主机目录:容器目录
      - nginx-conf:/etc/nginx/conf.d  # 命名卷:容器目录
    environment:         # 环境变量（键值对或列表形式）
      - TZ=Asia/Shanghai
      - DB_HOST=db
    env_file:            # 从文件加载环境变量
      - ./.env
    depends_on:          # 依赖服务（启动顺序：先启动 db，再启动 web）
      - db
    networks:            # 加入的网络
      - app-network
    command: nginx -g 'daemon off;'  # 覆盖容器默认启动命令
    healthcheck:         # 健康检查
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:     # 资源限制配置
      resources:
        limits: # 硬限制 - 容器不能超过此值
          cpus: '0.5' # 最多使用 0.5 个 CPU 核心
          memory: 512M # 最多使用 512MB 内存
        # 软限制 - 容器尽量使用不超过此值的资源
        reservations:
          cpus: '0.2'      # 保证至少 0.2 个 CPU 核心
          memory: 256M     # 保证至少 256MB 内存

networks:
  app-network:          # 网络名称
    driver: bridge      # 网络驱动（默认 bridge，可选 overlay 等）
    ipam:               # IP 地址管理（可选）
      config:
        - subnet: 172.20.0.0/16  # 子网
        - gateway: 172.20.0.1 # 网关

volumes:
  nginx-conf:           # 命名卷名称（可被多个服务挂载）
    driver: local       # 卷驱动（默认 local，可选 nfs 等）
    driver_opts:        # 驱动选项（如指定存储路径）
      type: 'none'
      device: '/opt/nginx/conf'
      o: 'bind'

```