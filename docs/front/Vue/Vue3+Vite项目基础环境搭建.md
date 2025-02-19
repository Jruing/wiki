# Vue3+Vite项目基础环境搭建
## 创建工程
```
# 创建目录
mkdir vue_demo
cd vue_demo
# 初始化项目
npm init
```

## 安装依赖
```
npm install vue
npm install vite
npm install @vitejs/plugin-vue
```

## 工程目录结构
```
- node_modules      存放项目第三方依赖。
- public      其他静态资源，如favicon.ico等静态资源。
- src
    - api      和服务端接口交互的文件。
    - assets     放置项目中的静态资源。
    - components    存放可复用的Vue组件。
    - router     配置项目路由信息。
    - store     全局状态管理。
    - views（或pages）    存放页面级别的Vue组件。
    - util     通用工具。
    - App.vue     Vue应用的根组件。
    - main.js     项目的入口文件。
- package.json     项目的配置文件，记录项目依赖的库及其版本等。
- README.md     项目的说明文档。
- index.html     项目在浏览器端的入口HTML文件。
```

## App.vue
```
<script setup>

</script>

<template>
    <div>
        My First Vue3 App
    </div>
</template>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
    margin-top: 60px;
    background-color: #fafafa;
}
</style>
```
## main.js
```
import {createApp} from 'vue';
import App from './App.vue';

// 创建Vue3实例对象
const app = createApp(App);
// 挂载Vue3实例到 #app 容器
app.mount('#app');
```
## index.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Vue App</title>
</head>
<body>
<div id="app"></div>
<script type="module" src="/src/main.js"></script>
</body>
</html>
```

## vite.config.js
```
import {defineConfig} from 'vite';
import vue from '@vitejs/plugin-vue';

// 设置服务配置信息
export default defineConfig({
    plugins: [vue()],
    server: {
        port: 3500,
        host: '0.0.0.0',
        open: true, // 启动服务时自动打开浏览器
    },
    build: {
        outDir: 'dist', // 构建输出目录
        assetsDir: 'assets', // 静态资源目录
        minify: 'terser', // 压缩代码，可选'esbuild'或'terser'
        terserOptions: {
            compress: {
                drop_console: true // 生产环境去除 console 语句
            }
        }
    }
});
```

## package.js
```
{
  "name": "vue_demo",
  "version": "1.0.0",
  "main": "index.js",
  "type": "module",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "dev": "vite",
    "build": "vite build"
  },
  "author": "",
  "license": "ISC",
  "description": "",
  "dependencies": {
    "@vitejs/plugin-vue": "^5.2.1",
    "vite": "^6.1.0",
    "vue": "^3.5.13"
  }
}
```

## 启动工程
```
npm run dev
```