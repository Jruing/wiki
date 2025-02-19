## 安装依赖
```
npm install vue-router
```

## 新增2个Demo组件
> components目录下创建两个文件DemoA.vue DemoB.vue
### DemoA.vue
```
<script setup>

</script>

<template>
  <div>
    Demo A. <br>
    <router-link to="/page/demoB">返回Demo B</router-link>
  </div>
</template>

<style scoped>
div {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
  background-color: #fafafa;
  font-size: 20px;
}
</style>
```
### DemoB.vue
```
<script setup>

</script>

<template>
  <div>
    Demo B. <br>
    <router-link to="/page/demoA">返回Demo A</router-link>
  </div>
</template>

<style scoped>
div {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
  background-color: #fafafa;
  font-size: 20px;
}
</style>
```
## 路由文件
> router目录下创建index.js
### index.js
```
import { createRouter, createWebHistory } from "vue-router";

// 定义静态路由信息
const routes = [
  {
    path: "/page/demoA",
    component: () => import("../components/DemoA.vue"),
  },
  {
    path: "/page/demoB",
    component: () => import("../components/DemoB.vue"),
  },
];

// 创建路由对象
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 导出路由对象
export default router;

```
## main.js引入路由
```
import {createApp} from 'vue';
import App from './App.vue';
// 引入路由
import router from './router';


// 创建Vue3实例对象
const app = createApp(App);
// 使用路由
app.use(router);
// 挂载Vue3实例到 #app 容器
app.mount('#app');
```

## App.vue
```
<script setup></script>

<template>
    <!-- 使用 router-view 渲染组件 -->
    <router-view v-slot="{ Component }">
        <!--  组件切换的时候，加上过渡效果  -->
        <transition>
            <!--   这里显示具体的组件内容   -->
            <component :is="Component" />
        </transition>
    </router-view>
</template>

<style></style>
```
## 启动工程
```
npm run dev
# 访问
http://localhost:3500/page/demoA
```

## \<router-link>标签
> `<router-link>`标签的作用是实现路由之间的跳转功能，默认情况下，`<router-link>`标签是采用超链接`<a>`标签显示的，通过to属性指定需要跳转的路由地址。当然，如果你不想使用默认的`<a>`标签，也可以使用tag属性自定义其他的标签。

- to

__字符串形式__
```
<router-link to="/page/demoA">Go to demoA</router-link>
```
__对象形式__
```
<router-link :to="{  path: '/page/demoA', params: { id: 123 } }">Go to demoA</router-link>
```
- replace
> 如果replace设置为true，导航时不会再浏览器的历史记录留下记录，而是替换当前记录
```
<router-link to="/page/demoA" replace>Go to demoA</router-link>
```
- append
> 假如当前url为http://baidu.com/aaa,使用append后就变成了http://baidu.com/aaa/about,如果未使用append,则是直接替换,变成http://baidu.com/about
```
<router-link to="/about" append>Go to About</router-link>
```
- tag
> 可以指定 `<router-link>` 渲染的 HTML 元素类型。默认是 `<a>`，但你可以将其改为其他元素，如 `<button>`。
```
<router-link to="/about" tag="button">Go to About</router-link>
```
- event
> 指定触发导航的事件类型。默认是 click，但你可以自定义。
```
<router-link to="/about" event="dblclick">Go to About</router-link>
```
- no-prefetch
> 在 Vue Router 的某些配置下，<router-link> 会预加载目标路由的组件以提高性能。如果不想预加载，可以设置 no-prefetch。

```
<router-link to="/about" no-prefetch>Go to About</router-link>
```
- active-class 和 exact-active-class
> * active-class：当链接匹配目标路由时，会自动添加这个类名。
> * exact-active-class：当链接精确匹配目标路由时，会自动添加这个类名。
```
<router-link to="/about" active-class="active" exact-active-class="exact-active">Go to About</router-link>
```

> 注意：`<router-link>`标签可以在不进行页面刷新的情况下，改变浏览器的URL地址，并触发相应路由的更新，使得`<router-view>`组件能够渲染与新路由对应的内容。


## \<router-view>标签
> `<router-view>` 是一个动态组件，用于渲染与当前 URL 匹配的路由组件。当用户导航到不同的路由时，`<router-view>` 会根据路由配置动态切换显示的组件，而不需要重新加载整个页面。
### 特点
> * 动态渲染组件：根据当前路由匹配的组件，动态渲染内容。
> * 支持嵌套路由：可以嵌套多个 `<router-view>`，实现复杂的页面结构。
> * 提供过渡效果：可以结合 Vue 的 `<transition>` 组件，为路由切换添加动画效果。

- name
> <router-view> 默认渲染的是默认的路由匹配项，但你可以通过 name 属性指定渲染特定的嵌套路由。

```
<router-view name="header"></router-view>
<router-view name="main"></router-view>
<router-view name="footer"></router-view>
```
## 路由跳转
> `router`对象中提供了几个路由跳转的方法，分别是`router.push()`、`router.replace()`、`router.go()`、`router.back()`、`router.forward()`这五个方法，其中最常用的是`router.push()`和`router.replace()`。
- `router.push()`方法作用：跳转到指定路由地址，不会替换历史访问记录中的当前路由
- `router.replace()`方法作用：跳转到指定路由地址，会替换历史访问记录中的当前路由
- `router.go(num)`方法作用：前进或者后退num个路由
- `router.back()`方法作用：后退1个路由，也就是等价于`router.go(-1)`的作用。
- `router.forward()`方法作用：前进1个路由，也就是等价于`router.go(1)`的作用。