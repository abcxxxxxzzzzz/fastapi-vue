// socket.js 全局方法实现
import Vue from 'vue'
import VueSocketIO from 'vue-socket.io'
import store from "@/store"
// import { getHostIp } from '@/api/admin/message' //获取后端动态ip地址
import { getToken } from '@/utils/cookies'


let socketIo, socketListener, socketEmitter

if (!getToken()) {
  const timerToken = setInterval(() => {
    console.count()
    // console.log('aa')
    if (!getToken()) return
    initSocket(getToken())
    window.clearInterval(timerToken)
  }, 1000)
} else { 
  initSocket(getToken())
}


// function getToken() {//获取登录标识---请修改为自己项目标识
//   return store.getters.access_token
// }

export function initSocket(token) {
  // const userId = store.state.user.username //获取登录标识---请修改为自己项目用户id
//   const ipResult = await getHostIp()
//   if (ipResult.code !== 0) return
//   const { ip, port } = ipResult.data
//   const protocol = window.location.protocol
//   const socketUrl = `${protocol}//${ip}:${port}?userId=${userId}`
//   console.log('socketUrl', socketUrl)
  const socketUrl = '/ws' //本地测试地址---nodejs服务代码放后面
  const socket = new VueSocketIO({
    debug: process.env.NODE_ENV !== 'production',
    options: {
      autoConnect: false //已通过验证，全局使用可默认打开，组件内使用则默认关闭，使用时在打开
    },
    connection: socketUrl
  })
  const { emitter, io, listener } = socket
  socketIo = io
  socketListener = listener
  socketEmitter = emitter

  if (process.env.NODE_ENV !== 'production') {// 与socket链接相关全局处理，与后端预定定义事件在组件内订阅使用
    io.on('connecting', () => { console.log('socketjs---正在连接') })
    io.on('connect', () => { console.log('socketjs---连接成功') })
    io.on('disconnect', () => { console.log('socketjs---断开连接') })
    io.on('connect_failed', () => { console.log('socketjs---连接失败') })
    io.on('error', () => { console.log('socketjs---错误发生，并且无法被其他事件类型所处理') })
    io.on('reconnect_attempt', () => { console.log('socketjs---触发尝试重新连接')})
    io.on('reconnecting', () => { console.log('socketjs---正在重连') })
    io.on('reconnect_failed', () => { console.log('socketjs---重连失败') })
    io.on('reconnect', () => { console.log('socketjs---重连成功') })
  }

  //   Vue.use(socket) //只是挂载了io模块，存在已加载页面无法订阅问题，不如不使用，自己挂载方便
  Object.defineProperty(Vue.prototype, '$socketIo', { value: socketIo })
  Object.defineProperty(Vue.prototype, '$socketListener', { value: socketListener })
  Object.defineProperty(Vue.prototype, '$socketEmitter', { value: socketEmitter })


//   return { socketIo, socketListener, socketEmitter } 
}

export default { socketIo, socketListener, socketEmitter } 
