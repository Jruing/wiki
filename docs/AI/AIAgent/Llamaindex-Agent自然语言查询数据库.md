## 安装
```
pip install llama-index
pip install llama-index-embeddings-text-embeddings-inference
pip install sqlalchemy
```

## 创建数据库
### 创建用户表
```
CREATE TABLE users (
    user_id INT PRIMARY KEY,                -- 用户唯一标识
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
(2,'Bob', '深圳市南山区', 'bob@example.com', '13900139000', '1985-08-20'),
(3,'Charlie', '广州市天河区', 'charlie@example.com', '13700137000', '1995-12-10'),
(4,'David', '深圳市南山区', 'david@example.com', '13600136000', '1988-03-25'),
(5,'Eve', '杭州市西湖区', 'eve@example.com', '13500135000', '1992-07-30');
```

## 主函数
```
from llama_index.core import SQLDatabase, Settings
from llama_index.core.agent import ReActAgent
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.tools import QueryEngineTool
from llama_index.embeddings.text_embeddings_inference import (
    TextEmbeddingsInference,
)
from sqlalchemy import create_engine

from llms_class import LLM
# 设置全局嵌入模型
Settings.embed_model = TextEmbeddingsInference(auth_token="sk-xxxxxx",
                                               base_url="https://api.siliconflow.cn/v1", model_name="BAAI/bge-m3")
Settings.llm = LLM(model_name="deepseek-ai/DeepSeek-R1-Distill-Qwen-14B", base_url="https://api.siliconflow.cn/v1",
                   api_key="sk-xxxxx")
# 创建数据库连接
engine = create_engine("sqlite:///test.db")
# 需要指定表名称
sql_database = SQLDatabase(engine, include_tables=["users"])
# 构建查询引擎，使用NL SQL Table Query Engine，支持自然语言查询，支持中文
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    # 表名称
    tables=["users"],
    llm=Settings.llm
)
user_tool = QueryEngineTool.from_defaults(
    query_engine,
    name="用户信息表",
    description="查询用户信息。"
)
# 构建ReActAgent，可以加很多函数，在这里只加了加法函数和部门人数查询函数。
agent = ReActAgent.from_tools([user_tool], verbose=True)
# 通过agent给出指令
response = agent.chat("统计深圳市南山区的用户数量")
print(response)
```
## 效果
```
> Running step 1e51c2ec-c82b-4f17-8833-e97c0c87ed78. Step input: 统计深圳市南山区的用户数量
Thought: The current language of the user is: 中文. I need to use a tool to help me answer the question.
Action: 用户信息表
Action Input: {'input': '深圳市南山区'}
Observation: 根据查询结果，以下是地址为“深圳市南山区”的用户信息：

- 用户ID 4：David，地址为深圳市南山区
- 用户ID 2：Bob，地址为深圳市南山区
> Running step eaf15ffb-bb70-4d5f-b6e2-2d91bce9f31f. Step input: None
Thought: 用户查询的是统计深圳市南山区的用户数量，我需要根据返回的信息给出答案。
Answer: 深圳市南山区的用户数量为2人。
深圳市南山区的用户数量为2人。
```