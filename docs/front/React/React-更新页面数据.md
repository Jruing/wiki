> useState 用于临时存储
```
import "./App.css";
import React from "react";
import { useState } from 'react';
function App() {
  // 定义count，setCount两个对象，setCount是count的setter函数，用于修改count的值，
  // useState(0)表示定义count的默认值为0(默认值可以是其他值，如false,"张三",{name:"zhangsan",age:18})，当组件刷新时，重新设置默认值
  const [count, setCount] = useState(0);
  const handleClick = () => {
    // 通过setCount方法对count的值进行修改
    setCount(count + 1);
  };
  return (
    <>
      {/* 渲染数据 */}
      <p>当前值：{count}</p>
      <button onClick={handleClick}>点击</button>
    </>
  );
} 

export default App;
```