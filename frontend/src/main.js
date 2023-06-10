import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

import ElementPlus from 'element-plus' // +
import 'element-plus/dist/index.css'   // +
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import { router } from './router' // +
import store from './store'
// import * as XLSX from 'xlsx'

const app = createApp(App)


// app.provide('XLSX', XLSX)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }

app.use(router)
app.use(ElementPlus,{ locale: zhCn }) // +
app.use(store)


import 'virtual:windi.css'   // + 
import 'nprogress/nprogress.css'

import './dependencies/permission.js'
import permission from  './dependencies/has-permission.js'


import VXETable from 'vxe-table'
import 'vxe-table/lib/style.css'
// import './utils/socket.js'  //使用全局挂载







app.use(permission)
app.use(VXETable)
app.mount('#app')    // +
