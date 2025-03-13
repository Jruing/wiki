## 简介
LLM API 管理 & 分发系统，支持 OpenAI、Azure、Anthropic Claude、Google Gemini、DeepSeek、字节豆包、ChatGLM、文心一言、讯飞星火、通义千问、360 智脑、腾讯混元等主流模型，统一 API 适配，可用于 key 管理与二次分发。单可执行文件，提供 Docker 镜像，一键部署，开箱即用项目地址：https://github.com/songquanpeng/one-api
## Docker部署安装
```
docker volume create oneapi
docker run --name oneapi -d --restart=always -p 3000:3000 -e TZ=Asia/Shanghai -v oneapi:/data justsong/one-api:latest
```
## 访问地址
> http://ip:3000


## 默认账号密码
> root/123456

## 创建渠道

![image-20250313173546822](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250313173546822.png)

## 创建令牌

![image-20250313173651383](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250313173651383.png)

![image-20250313173747444](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20250313173747444.png)

## API调用

> Base URL:http://ip:3000
>
> API key: 上面的令牌
