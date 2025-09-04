## 安装
```
pip install llama-index
pip install peewee
```

## 创建数据库
### 创建用户表
```
CREATE TABLE users (
    user_id INT PRIMARY KEY,                -- 用户唯一标识，自动递增
    name VARCHAR(255) NOT NULL,             -- 用户名称，不允许为空
    address VARCHAR(255),                   -- 用户地址，允许为空
    email VARCHAR(255),                     -- 用户邮箱，允许为空
    phone_number VARCHAR(20),               -- 用户手机号，允许为空
    birthday DATE                           -- 用户生日，允许为空
);
```
### 测试数据
```
INSERT INTO users (id,name, address, email, phone_number, birthday) VALUES
(1,'Alice', '北京市朝阳区', 'alice@example.com', '13800138000', '1990-05-15'),
(2,'Bob', '上海市浦东新区', 'bob@example.com', '13900139000', '1985-08-20'),
(3,'Charlie', '广州市天河区', 'charlie@example.com', '13700137000', '1995-12-10'),
(4,'David', '深圳市南山区', 'david@example.com', '13600136000', '1988-03-25'),
(5,'Eve', '杭州市西湖区', 'eve@example.com', '13500135000', '1992-07-30');
```
## 创建工具函数
```
from peewee import *

db = SqliteDatabase('test.db')
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class UserInfo(BaseModel):
    user_id = IntegerField()
    name = CharField()
    address = CharField()
    email = CharField()
    phone_number = CharField()
    birthday = DateField()

    class Meta:
        table_name = "users"

# 具体的工具函数，此处需要定义字段，模型将根据用户提供的信息自动匹配字段(受用户输入影响很大)
def getuserinfo(name: str = None, email: str = None, address: str = None, birthday: str = None,
                phone_number: str = None) -> dict:
    """根据用户姓名、邮箱、地址查询用户信息"""
    query = UserInfo.select(UserInfo.user_id, UserInfo.name, UserInfo.address, UserInfo.email, UserInfo.phone_number,
                            UserInfo.birthday)
    if name:
        query = query.where(UserInfo.name == name)
    if birthday:
        query = query.where(UserInfo.birthday == birthday)
    if phone_number:
        query = query.where(UserInfo.phone_number == phone_number)
    if address:
        query = query.where(UserInfo.address == address)
    if email:
        query = query.where(UserInfo.email == email)
    # rs = query.dicts()
    query_result = [user.__data__ for user in query]
    if query_result:
        query_result[0]["birthday"] = str(query_result[0]["birthday"])
    print(query_result)
    return {"result": query_result}
```
## 自定义LLM
```
from typing import Any, Generator

from llama_index.core.llms import (
    CustomLLM,
    CompletionResponse,
    LLMMetadata,
)
from llama_index.core.llms.callbacks import llm_completion_callback
from openai import OpenAI
from pydantic import Field  


# 定义新的LLM类，继承自CustomLLM基类
class LLM(CustomLLM):
    api_key: str = Field(default="api_key")
    base_url: str = Field(default="http://127.0.0.1:8000/v1")
    model_name: str = Field(default="glm-4-flash")
    client: OpenAI = Field(default=None, exclude=True)  # 显式声明 client 字段

    def __init__(self, api_key: str, base_url: str, model_name: str = model_name, **data: Any):
        super().__init__(**data)
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)  # 使用传入的api_key和base_url初始化 client 实例

    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""
        return LLMMetadata(
            model_name=self.model_name,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        response = self.client.chat.completions.create(model=self.model_name,
                                                       messages=[{"role": "user", "content": prompt}])
        if hasattr(response, 'choices') and len(response.choices) > 0:
            response_text = response.choices[0].message.content
            return CompletionResponse(text=response_text)
        else:
            raise Exception(f"Unexpected response format: {response}")

    @llm_completion_callback()
    def stream_complete(
            self, prompt: str, **kwargs: Any
    ) -> Generator[CompletionResponse, None, None]:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        try:
            for chunk in response:
                chunk_message = chunk.choices[0].delta
                if not chunk_message.content:
                    continue
                content = chunk_message.content
                yield CompletionResponse(text=content, delta=content)

        except Exception as e:
            raise Exception(f"Unexpected response format: {e}")
```
## 主函数
> 这里用的是硅基流动,新用户注册送14元的额度,这是邀请连接：https://cloud.siliconflow.cn/i/Fvcyk52x 通过邀请链接注册我也可以获得14元额度,也可以使用其他厂商的
```
# encoding:utf8

from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool

from agent_tools.getUserInfo import getuserinfo
from llms_class import LLM


class UserInfoAgent:
    def __init__(self):
        # model_name 模型名称
        # base_url 接口地址
        # api_key 自己的api_key
        self.llm = LLM(model_name="deepseek-ai/DeepSeek-R1-Distill-Qwen-14B", base_url="https://api.siliconflow.cn/v1",
                       api_key="sk-xxxx")
        self.tools = []

    def add_tool(self, tool):
        self.tools.append(tool)

    def chat(self, query):
        # 添加自定义工具,这里的getuserinfo函数是自定义的函数，需要添加到工具列表中
        userinfo_tool = FunctionTool.from_defaults(fn=getuserinfo)
        self.tools.append(userinfo_tool)
        # 创建ReActAgent实例
        agent = ReActAgent.from_tools(self.tools, llm=self.llm, verbose=True)
        return agent.chat(query)

# 调用
if __name__ == '__main__':
    userinfo_agent = UserInfoAgent()
    # 查询用户Eve的所有信息,如果要查询表数据总数，需要自定义新的工具函数用于获取表数据总数
    userinfo_agent.chat("查询用户Eve的所有信息")
```
## 效果
```
> Running step 71672083-3e6e-4928-9386-4357d913c675. Step input: 查询用户Eve的所有信息
Thought: The current language of the user is: 中文. I need to use a tool to help me answer the question.
Action: getuserinfo
Action Input: {'name': 'Eve'}
Observation: {'result': [{'user_id': 5, 'name': 'Eve', 'address': '杭州市西湖区', 'email': 'eve@example.com', 'phone_number': '13500135000', 'birthday': '1992-07-30'}]}
> Running step f326ef97-d301-4172-a74a-b7ef89e25875. Step input: None
Thought: (Implicit) I can answer without any more tools!
Answer: Answer: Eve的用户信息如下：
- 用户ID：5
- 姓名：Eve
- 地址：杭州市西湖区
- 邮箱：eve@example.com
- 电话号码：13500135000
- 生日：1992年7月30日
```