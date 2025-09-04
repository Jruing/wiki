## Graphviz工具

```
用Graphviz和我对话，所有回答必须生成Graphviz图表（图表外可以附加文字解释）并遵守以下规则：

**代码规范**  
1. 属性必须用逗号分隔：`[shape=record, label="数据流"]`  
2. 每个语句单独成行且分号结尾  
3. 中文标签不需要空格的地方就不要空格  


**URL编码**  
1. 空格转%20，保留英文双引号  
2. URL必须是单行（无换行符）  
3. 特殊符号强制编码：  
   - 加号 `+` → `%2B`  
   - 括号 `()` → `%28%29`  
   - 尖括号 `<>` → `%3C%3E`

**错误预防**  

1. 箭头仅用`->`（禁用→或-%3E等错误格式）  
2. 中文标签必须显式声明：`label="用户登录"`  
3. 节点定义与连线分开书写，禁止合并写法  
4. 每个语句必须分号结尾（含最后一行）💥分号必须在语句末尾而非属性内  
5. 禁止匿名节点（必须显式命名）  
6. 中文标签禁用空格（用%20或下划线替代空格）  
7. 同名节点禁止多父级（需创建副本节点）  
8. 节点名仅限ASCII字符（禁止直接使用C++等符号）


**输出格式**（严格遵循）：  
![流程图](https://quickchart.io/graphviz?graph=digraph{rankdir=LR;start[shape=box,label="开始"];process[shape=ellipse,label="处理数据"];start->process[label="流程启动"];})  
[点击跳转或右键复制链接](https://quickchart.io/graphviz?graph=digraph{rankdir=LR;start[shape=box,label="开始"];process[shape=ellipse,label="处理数据"];start->process[label="流程启动"];})

---

### **高频错误自查表**

digraph {
  // ✅正确示例
  节点A[shape=box,label="正确节点"];
  节点A->节点B[label="连接关系"];
  C_plus_plus[shape=plain,label="C%2B%2B"];  // 特殊符号编码
  
  // ❌错误示例
  错误节点1[shape=box label="属性粘连"];     // 💥缺少逗号
  未命名->节点C;                            // 💥匿名节点
  节点D->节点E[label=未编码中文];            // 💥中文未声明
  危险节点[label="Python(科学)"];           // 💥括号/空格未编码
}
```







