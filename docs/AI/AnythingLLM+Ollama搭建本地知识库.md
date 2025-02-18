# AnythingLLM+Ollama搭建本地知识库



## Ollama

### 下载

https://ollama.com/download

### 获取大模型

大模型列表：https://ollama.com/library

```
# 拉取大模型
ollama run qwen2.5:7b

writing manifest
success
>>> /?
Available Commands:
  /set            Set session variables
  /show           Show model information
  /load <model>   Load a session or model
  /save <model>   Save your current session
  /clear          Clear session context
  /bye            Exit
  /?, /help       Help for a command
  /? shortcuts    Help for keyboard shortcuts

Use """ to begin a multi-line message.

# 加载qwen2.5:7b模型
>>> /load qwen2.5:7b
Loading model 'qwen2.5:7b'
>>> Send a message (/? for help)
```



## AnythingLLM

###  下载

https://anythingllm.com/download

### 安装

#### 一、开始使用

![image-20240928152516143](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202409281616776.png)

#### 二、 选择LLM提供商，我们使用的是上面安装好的Ollama

![image-20240928152940258](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202409281616993.png)

#### 三、 创建工作区

![image-20240928153151822](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202409281616928.png)

#### 四、 修改一些全局参数

![image-20240928153302793](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202409281616975.png)

#### 五、修改Anything 语言

![image-20240928153346845](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202409281649540.png)

#### 六、后续根据自身情况切换LLM提供商，可以换成OpenAi等其他LLM提供商

![image-20240928153554064](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202409281616792.png)

#### 七、设置文本拆分

![image-20240928154216480](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202409281616563.png)

#### 八、修改工作区配置

![image-20240928154849621](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202409281616452.png)

#### 九、测试使用

![image-20240928154405518](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202409281616420.png)

## 搭建本地知识库

#### 一、增加知识库并上传本地文档

![image-20240928155033571](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202409281616720.png)

> 创建文件夹，则文件夹位置在`C:\Users\用户名\AppData\Roaming\anythingllm-desktop\storage\documents` 目录下,后面文档都可以手动放到这个目录下，也可以不创建，使用默认位置

![image-20240928155221659](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202409281616057.png)

![image-20240928160627276](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202409281616567.png)

#### 二、修改工作区设置

![image-20240928162413599](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202409281624761.png)

#### 三、测试本地知识库

![image-20240928162802497](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202409281628655.png)

![image-20240928162855859](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202409281628037.png)

#### 四、生成API KEY

> 生成AnythingLLM API KEY，方便其他应用程序调用

![image-20240928164816351](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/202409281648509.png)
