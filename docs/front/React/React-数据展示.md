> 用{}包裹变量后，除了可以填充内容以外，还可以填充标签属性的值

# App.css
```
.p1 {
  color:#61dafb
}
```
# App.js
```
import "./App.css";
const user = {
  name: "Jruing",
  age: 27,
  github: "https://github.com/Jruing",
};

const p_style = {
  name: "p1",
};

function App() {
  return (
    <>
      {/* 填充内容 */}
      <p>姓名：{user.name}</p>
      {/* 填充className的值 */} 
      <p className={p_style.name}>年龄：{user.age}</p>
      <a href={user.github}>github</a>
    </>
  );
}

export default App;
```