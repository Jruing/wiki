# ServerLess学习笔记-搭建FnProject示例

## 初始化函数目录

```
# 初始化 fn_demo1
[root@VM-24-9-centos serverless]# fn init --runtime python fn_demo1
Creating function at: ./fn_demo1
Unable to get latest FDK version, using default
Function boilerplate generated.
func.yaml created.

# 初始化 fn_demo2
[root@VM-24-9-centos serverless]# fn init --runtime python fn_demo2
Creating function at: ./fn_demo2
Function boilerplate generated.
func.yaml created.
```

## 创建应用

```
[root@VM-24-9-centos serverless]# fn create app fn_app
Successfully created app:  fn_app
```

## 修改函数代码

> 下面为函数`fn_demo1`的修改，`fn_demo2` 参考`fn_demo1`进行修改

```
[root@VM-24-9-centos serverless]# cd fn_demo1/
[root@VM-24-9-centos fn_demo1]# ls
func.py  func.yaml  requirements.txt
[root@VM-24-9-centos fn_demo1]# ll
total 12
-rw-r--r-- 1 root root 576 Oct 20 17:09 func.py
-rw-r--r-- 1 root root 207 Oct 20 17:10 func.yaml
-rw-r--r-- 1 root root   3 Oct 20 17:10 requirements.txt

# 修改func.py
[root@VM-24-9-centos fn_demo1]# vi func.py 
import io
import json
import logging

from fdk import response


def handler(ctx, data: io.BytesIO = None):
    name = "fn_demo1" # 将此处的World修改为fn_demo1方便测试调用后的展示结果
    try:
        body = json.loads(data.getvalue())
        name = body.get("name")
    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex))

    logging.getLogger().info("Inside Python Hello World function")
    return response.Response(
        ctx, response_data=json.dumps(
            {"message": "Hello {0}".format(name)}),
        headers={"Content-Type": "application/json"}
```

>func.yaml配置文件字段详解
>
>```
>schema_version: 20180708  #标识此函数文件的架构版本
>name: fn_demo1  #函数的名称。与目录名称匹配
>version: 0.0.1 #版本号：从 0.0.1 自动开始
>runtime: python #运行时设置的语言环境
>entrypoint: /python/bin/fdk /function/func.py handler #调用函数时要调用的可执行文件的名称
>memory: 256 #函数的最大内存大小，单位：MB
>```

## 部署应用/函数

> 将函数`fn_demo1` 和`fn_demo2`分别与`fn_app`关联并部署,部署`fn_demo2`与`fn_demo1`步骤一致

```
# 进入函数目录
[root@VM-24-9-centos serverless]# cd fn_demo1/
# 部署函数
[root@VM-24-9-centos fn_demo1]# fn --verbose deploy --app fn_app --local
Deploying fn_demo1 to app: fn_app
Bumped to version 0.0.4
Using Container engine docker
Building image fn_demo1:0.0.4 
Dockerfile content
-----------------------------------
FROM fnproject/python:3.9-dev as build-stage
WORKDIR /function
ADD requirements.txt /function/

			RUN pip3 install --target /python/  --no-cache --no-cache-dir -r requirements.txt &&\
			    rm -fr ~/.cache/pip /tmp* requirements.txt func.yaml Dockerfile .venv &&\
			    chmod -R o+r /python
ADD . /function/
RUN rm -fr /function/.pip_cache
FROM fnproject/python:3.9
WORKDIR /function
COPY --from=build-stage /python /python
COPY --from=build-stage /function /function
RUN chmod -R o+r /function
ENV PYTHONPATH=/function:/python
ENTRYPOINT ["/python/bin/fdk", "/function/func.py", "handler"]
-----------------------------------
FN_REGISTRY:  FN_REGISTRY is not set.
Current Context:  default
[+] Building 120.6s (17/17) FINISHED                                                                                                                     
 => [internal] load build definition from Dockerfile2218814693                                                                                      0.0s
 => => transferring dockerfile: 643B                                                                                                                0.0s
 => [internal] load .dockerignore                                                                                                                   0.0s
 => => transferring context: 2B                                                                                                                     0.0s
 => [internal] load metadata for docker.io/fnproject/python:3.9                                                                                     0.7s
 => [internal] load metadata for docker.io/fnproject/python:3.9-dev                                                                                 0.8s
 => [build-stage 1/6] FROM docker.io/fnproject/python:3.9-dev@sha256:2a257fac48519801b646c7217b151049bfaa29e75c0d8cdd9469e6db86a45adc               0.0s
 => [stage-1 1/5] FROM docker.io/fnproject/python:3.9@sha256:8af5441307d08e86b79b46675050cb4b98b251bd980b32fc58764702710399ab                       0.0s
 => [internal] load build context                                                                                                                   0.0s
 => => transferring context: 952B                                                                                                                   0.0s
 => CACHED [build-stage 2/6] WORKDIR /function                                                                                                      0.0s
 => CACHED [build-stage 3/6] ADD requirements.txt /function/                                                                                        0.0s
 => [build-stage 4/6] RUN pip3 install --target /python/  --no-cache --no-cache-dir -r requirements.txt &&       rm -fr ~/.cache/pip /tmp* requi  118.8s
 => [build-stage 5/6] ADD . /function/                                                                                                              0.0s
 => [build-stage 6/6] RUN rm -fr /function/.pip_cache                                                                                               0.2s 
 => CACHED [stage-1 2/5] WORKDIR /function                                                                                                          0.0s 
 => [stage-1 3/5] COPY --from=build-stage /python /python                                                                                           0.1s 
 => [stage-1 4/5] COPY --from=build-stage /function /function                                                                                       0.1s 
 => [stage-1 5/5] RUN chmod -R o+r /function                                                                                                        0.2s 
 => exporting to image                                                                                                                              0.1s
 => => exporting layers                                                                                                                             0.1s
 => => writing image sha256:5700ac5e7fc00f10b9c812292283184c25be858c8cf537e9b15d1d3dec80ef96                                                        0.0s
 => => naming to docker.io/library/fn_demo1:0.0.1                                                                                                   0.0s

Updating function fn_demo1 using image fn_demo1:0.0.1...
```

### 查看生成的服务镜像

```
[root@VM-24-9-centos fn_demo2]# docker images
REPOSITORY                   TAG       IMAGE ID       CREATED          SIZE
fn_demo2                     0.0.2     82a9bc7b0f7f   59 seconds ago   174MB
fn_demo1                     0.0.4     5700ac5e7fc0   2 minutes ago    174MB
```

## 获取函数信息

> 查看`fn_demo1`的信息

```
[root@VM-24-9-centos serverless]# ./fn inspect function fn_app fn_demo1
{
	"annotations": {
		"fnproject.io/fn/invokeEndpoint": "http://localhost:8080/invoke/01HD66V4V6NG8G00RZJ000000H" # 函数的调用地址
	},
	"app_id": "01HD65NGGGNG8G00RZJ000000G",
	"created_at": "2023-10-20T09:32:11.494Z",
	"id": "01HD66V4V6NG8G00RZJ000000H",
	"idle_timeout": 30,
	"image": "fn_demo1:0.0.4",
	"memory": 256,
	"name": "fn_demo1",
	"timeout": 30,
	"updated_at": "2023-10-20T09:32:11.494Z"
}
```

## 调用函数

### 通过fn调用函数

```
[root@VM-24-9-centos serverless]# fn invoke fn_app fn_demo1
{"message": "Hello fn_demo1"}
[root@VM-24-9-centos serverless]# fn invoke fn_app fn_demo2
{"message": "Hello fn_demo2"}
```

### 通过Curl调用函数

```
[root@VM-24-9-centos serverless]# curl -X "POST" -H "Content-Type: application/json" -d '{"name":"fn_demo1"}' http://localhost:8080/invoke/01HD66V4V6NG8G00RZJ000000H
{"message": "Hello fn_demo1"}
[root@VM-24-9-centos serverless]# curl -X "POST" -H "Content-Type: application/json" -d '{"name":"fn_demo2"}' http://localhost:8080/invoke/01HD66XF41NG8G00RZJ000000J
{"message": "Hello fn_demo2"}
```

