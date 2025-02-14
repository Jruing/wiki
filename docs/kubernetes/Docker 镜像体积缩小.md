

## 背景

> 手动构建的 Docker 镜像如果体积过大，可以利用 `slim` 工具来优化和减小其体积。`slim` 不仅能够有效地缩减镜像大小，还有以下额外好处：
>
> 1. **减少攻击面**：通过精简镜像，移除了不必要的文件和依赖，从而减少了潜在的安全漏洞和攻击面。
> 2. **降低安全风险**：较小的镜像意味着更少的软件组件，这有助于降低由于软件漏洞带来的安全风险。
> 3. **提高传输效率**：体积更小的镜像可以更快地被下载和部署，提高了镜像分发和更新的效率。
> 4. **优化资源使用**：在资源受限的环境中，较小的镜像可以减少存储和内存的使用，提高系统性能。
>
> `slim` 工具除了缩小镜像体积之外，还有其他的作用和优势。更多详细信息和使用指南，请访问项目的官方文档页面。通过深入了解和应用 `slim`，你可以构建更加轻量级、安全和高效的 Docker 镜像。
>
> Github地址：https://github.com/slimtoolkit/slim

## 安装

```
# 下载slim
wget https://github.com/slimtoolkit/slim/releases/download/1.40.11/dist_linux.tar.gz
# 解压
tar -zxvf dist_linux.tar.gz
# 移动文件到/usr/local/bin中
mv dist_linux/slim /usr/local/bin/
mv dist_linux/slim-sensor /usr/local/bin/
```

## 更新slim(联网更新)

```
slim update
```

## 应用

```
# 查看现有docker镜像
[root@localhost ~]# docker images
REPOSITORY   TAG           IMAGE ID       CREATED        SIZE
nginx        latest        fffffc90d343   4 months ago   188MB
# 压缩镜像 slim build <镜像名称>/<镜像id>
[root@localhost ~]# slim build fffffc90d343
REPOSITORY                TAG           IMAGE ID       CREATED          SIZE
nginx.slim                latest        e200c2386f30   18 seconds ago   13.3MB
nginx                     latest        fffffc90d343   4 months ago     188MB

nginx.slim 就是压缩后的镜像文件，镜像体积缩小了14倍
```

