```
import "./App.css";
import React from "react";
// 定义用户信息组件，需要用户名和年龄2个参数
function UserInfo({username,age}) {
  return (
    <>
      <p>姓名：{username}</p>
      <p>年龄：{age}</p>
    </>
  );
}

function App() {

  return (
    <>
      <UserInfo username="张三" age={18}/>
    </>
  );
}

export default App;
```