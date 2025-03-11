```
import "./App.css";

function App() {
  // 定义响应事件函数
  function handleClick() {
    alert("你点击了按钮");
  }
  function handleChange(e) {
    console.log(e.target.value);
  }
  return (
    <>
      // 调用点击事件函数
      <button onClick={handleClick}>点击</button>
      <input onChange={handleChange} placeholder="请输入内容" />
    </>
  );
} 

export default App;
```
