```
import "./App.css";
const colorList = ["red", "blue", "yellow"];
const colorItem = colorList.map((item,index) => (
  <li style={{ color: item }}>{index}-{item}</li>
));

function App() {
  return (
    <>
      <ul>{colorItem}</ul>
    </>
  );
}

export default App;
```