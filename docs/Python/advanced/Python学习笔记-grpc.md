# Python学习笔记-grpc

## grpc简介

> gRPC 可以使用 Protocol Buffers 作为其接口定义语言 (**IDL**) 和其底层消息交换格式

## 安装依赖

```
pip install grpcio grpcio-tools
```

## 例子

- user.proto

```
syntax = "proto3";  // 指定使用 proto3 语法

package example;    // 定义包名，防止命名冲突

// 定义一个 User 消息结构
message User {
  int32 id = 1;      // 用户 ID，整数类型 （字段编号为 1）
  string name = 2;   // 用户姓名，字符串类型 （字段编号为 2）
  int32 age = 3;  // 用户年龄，字符串类型 （字段编号为 3）
}

// 定义请求参数结构
message GetUserRequest {
  int32 id = 1;// 用户 ID（字段编号为 1）
}

// 定义响应体结构
message GetUserResponse {
  int32 code = 1;// 状态码（字段编号为 1）
  string message = 2;// 状态信息（字段编号为 2）
  User user = 3;// 返回用户对象（字段编号为 3）
}


// 定义服务
service UserService {
  // 定义一个远程调用方法
  rpc GetUser (GetUserRequest) returns (GetUserResponse);
}
```

- 生成代码

```
python -m grpc_tools.protoc -I=services\user --python_out=services\user --grpc_python_out=services\user --proto_path=. users.proto 
```

- 参数详解
  - `-I=.`：指定 `.proto` 文件的搜索路径（当前目录）。
  - `--python_out=.`：指定生成的 Python 消息类文件的输出目录（当前目录）。
  - `--grpc_python_out=.`：指定生成的 Python 服务类文件的输出目录（当前目录）。
  - `--proto_path=.`: 指定 `.proto` 文件的根搜索路径。
  - `users.proto`：输入的 `.proto` 文件。
- server.py

```
# encoding:utf8
from concurrent import futures

import grpc

import users_pb2
import users_pb2_grpc

# 实现UserService接口
class UserService(users_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        print(request)
        # 返回上面proto文件中定义的返回值结构信息
        return users_pb2.GetUserResponse(
            code=1,
            message="成功",
            user=users_pb2.User(
                id=1,
                name="张三",
                age=19
            )
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    # 对外暴露端口
    server.add_insecure_port('[::]:50051')
    print("Server started on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

```

- client.py

```
import grpc

import users_pb2
import users_pb2_grpc


def run():
    # 连接到服务器
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = users_pb2_grpc.UserServiceStub(channel)
        # 构造请求(请求参数的字段以proto定义的为准)
        response = stub.GetUser(users_pb2.GetUserRequest(id=1))
        print(f"Greeter client received: {response}")


if __name__ == '__main__':
    run()
```

- 项目结构

```
service/user
├── user.proto          # Protobuf 定义文件
├── user_pb2.py         # 生成的消息类
├── user_pb2_grpc.py    # 生成的服务类
├── server.py           # 服务端代码
└── client.py           # 客户端代码
```

