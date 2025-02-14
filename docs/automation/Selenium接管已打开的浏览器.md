## 启动谷歌浏览器远程调试
`chrome.exe --remote-debugging-port=9222 --user-data-dir="某个存在的文件夹地址"`

## 新建python文件
```
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
 
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") # 端口即远程调试定义的端口
chrome_driver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe" # webdriver路径
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
print(driver.title)
```

