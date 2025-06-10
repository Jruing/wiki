### **Fetch API 完全手册**

`fetch` 是现代 JavaScript 中用于发起网络请求的标准 API

### **基本语法**
```javascript
fetch(url [, options])
  .then(response => {
    // 处理响应
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    return response.json(); // 或 response.text()/blob()/formData()
  })
  .then(data => {
    // 使用解析后的数据
  })
  .catch(error => {
    // 处理错误
  });
```


### **核心参数**
#### 1. **`url`**
请求的目标 URL，可以是绝对路径或相对路径。

#### 2. **`options`**（可选）
配置请求的对象，常见属性：
```javascript
{
  method: 'GET',          // HTTP 方法 (GET, POST, PUT, DELETE, etc.)
  headers: {              // 请求头
    'Content-Type': 'application/json',
    'Authorization': 'Bearer token'
  },
  body: JSON.stringify(data), // 请求体（GET 请求不能有 body）
  mode: 'cors',               // 请求模式 (cors, no-cors, same-origin)
  credentials: 'same-origin', // 携带凭证 (omit, same-origin, include)
  cache: 'default',           // 缓存策略
  redirect: 'follow',         // 重定向处理
  referrer: 'client',         // 引用来源
  signal: AbortSignal         // 中断请求的信号
}
```


### **响应处理**
`fetch` 返回的 `response` 对象包含以下常用属性和方法：

#### **属性**
- `response.ok`：布尔值，表示状态码是否在 200-299 之间。
- `response.status`：HTTP 状态码（如 200, 404, 500）。
- `response.statusText`：状态文本（如 "OK", "Not Found"）。
- `response.headers`：响应头（可通过 `get(name)` 访问）。
- `response.url`：最终请求的 URL（处理重定向后）。

#### **方法**
- `response.json()`：解析为 JSON 对象。
- `response.text()`：解析为文本。
- `response.blob()`：解析为二进制文件。
- `response.formData()`：解析为 FormData 对象。
- `response.arrayBuffer()`：解析为 ArrayBuffer。


### **常见请求示例**

#### 1. **GET 请求（获取 JSON 数据）**
```javascript
fetch('https://api.example.com/data')
  .then(res => res.json())
  .then(data => console.log(data));
```

#### 2. **POST 请求（发送 JSON 数据）**
```javascript
fetch('https://api.example.com/submit', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'John',
    age: 30
  })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

#### 3. **上传文件**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('https://api.example.com/upload', {
  method: 'POST',
  body: formData
});
```

#### 4. **携带 Cookie**
```javascript
fetch('https://api.example.com/data', {
  credentials: 'include' // 跨域请求也携带 Cookie
});
```

#### 5. **设置自定义请求头**
```javascript
fetch('https://api.example.com/data', {
  headers: {
    'X-Custom-Header': 'value',
    'Authorization': 'Bearer token'
  }
});
```


### **高级用法**

#### 1. **请求超时控制**
```javascript
const controller = new AbortController();
const signal = controller.signal;

setTimeout(() => controller.abort(), 5000); // 5 秒后中断请求

fetch('https://api.example.com/data', { signal })
  .then(res => res.json())
  .catch(err => {
    if (err.name === 'AbortError') {
      console.log('请求超时');
    }
  });
```

#### 2. **流式响应处理**
```javascript
fetch('https://api.example.com/large-data')
  .then(response => {
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    return reader.read().then(function processResult(result) {
      if (result.done) return;
      
      const chunk = decoder.decode(result.value, { stream: true });
      console.log('收到数据块:', chunk);
      
      return reader.read().then(processResult);
    });
  });
```

#### 3. **同时处理多个请求**
```javascript
Promise.all([
  fetch('https://api.example.com/data1'),
  fetch('https://api.example.com/data2')
])
  .then(responses => Promise.all(responses.map(res => res.json())))
  .then(dataArray => {
    console.log('数据1:', dataArray[0]);
    console.log('数据2:', dataArray[1]);
  });
```


### **错误处理**
`fetch` 只有在网络故障或请求被阻止时才会抛出错误，HTTP 错误（如 404、500）不会触发 `catch`，需要手动检查：

```javascript
fetch('https://api.example.com/nonexistent')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  })
  .catch(error => {
    console.error('请求失败:', error.message);
  });
```


### **兼容性与 Polyfill**
- **浏览器支持**：Chrome 42+、Firefox 39+、Safari 10.1+、Edge 14+。
- **IE 兼容性**：完全不支持，需使用 [fetch polyfill](https://github.com/github/fetch)。

安装 polyfill：
```bash
npm install whatwg-fetch
```

在代码中引入：
```javascript
import 'whatwg-fetch'; // 或在 HTML 中直接引入 <script src="path/to/fetch.js"></script>
```


### **常见问题**

#### 1. **CORS（跨域资源共享）问题**
- 需服务器端设置正确的响应头（如 `Access-Control-Allow-Origin`）。
- 使用 `mode: 'no-cors'` 只能获取有限的响应信息。

#### 2. **POST 请求的 Content-Type**
- 发送 JSON：`'Content-Type': 'application/json'` + `JSON.stringify()`。
- 发送表单数据：使用 `FormData` 对象（无需手动设置 Content-Type）。

#### 3. **中断请求**
使用 `AbortController`（见上文超时控制示例）。


### **完整示例：封装 fetch 函数**
```javascript
async function customFetch(url, options = {}) {
  try {
    // 设置默认选项
    const defaultOptions = {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      },
      credentials: 'same-origin',
      mode: 'cors'
    };

    // 合并选项
    const mergedOptions = { ...defaultOptions, ...options };

    // 处理 JSON 数据
    if (mergedOptions.body && typeof mergedOptions.body === 'object' && 
        !(mergedOptions.body instanceof FormData)) {
      mergedOptions.headers['Content-Type'] = 'application/json';
      mergedOptions.body = JSON.stringify(mergedOptions.body);
    }

    // 发起请求
    const response = await fetch(url, mergedOptions);

    // 检查响应状态
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // 根据 Content-Type 自动解析响应
    const contentType = response.headers.get('Content-Type');
    if (contentType?.includes('application/json')) {
      return response.json();
    } else if (contentType?.includes('text/')) {
      return response.text();
    } else {
      return response.blob();
    }
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
}

// 使用示例
customFetch('https://api.example.com/data')
  .then(data => console.log(data))
  .catch(err => console.error(err));
```