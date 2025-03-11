# 简介
> 若需要返回多个JSX标签必须有且只有一个父标签，

```
import './App.css';

function App() {
  return (
    // 只能有一个父标签，可以为<></>,也可以为<div></div>等其他标签
    <>
      <h1>Hello, world!</h1>
      <h2>这是一个二级标题</h2>
    </>
  );
}

export default App;
```