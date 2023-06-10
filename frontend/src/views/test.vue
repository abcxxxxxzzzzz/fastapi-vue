//demo.vue  订阅事件与销毁在组件中进行
<template>
  <div> 
    <!-- <button>{{ value }}</button> -->
    <!-- <button @click="closeSocket">断开链接</button>
    <button @click="submsgContent(true)">订阅事件</button>
    <button @click="submsgContent(false)">取消订阅事件</button>
    <button @click="socketSendmsg">发送数据</button>
    <button @click="lockResult">查看链接参数</button> -->



        <el-button type="primary" size="default" @click="btn">send</el-button>
        
        <el-divider direction="horizontal" content-position="left"></el-divider>
        


  </div>
</template>
<script setup>

import { ref } from 'vue'

const insert_total = ref(0)
const error_total = ref(0)
const error_data = ref([])



let ws_url = 'ws://' + window.location.host + '/api/admin/ws'

var ws = new WebSocket(ws_url);
ws.onmessage = function(event){
    console.log(event.data)
}

setInterval(() => {
    ws.send('aa')
},1000)





// onBeforeMount(() => {


// })



// import { onBeforeUnmount, onMounted } from 'vue'
// import { initSocket }  from '@/utils/socket.js'


// const {
//     socketIo, socketListener, socketEmitter
// } = initSocket({

// })



// onBeforeUnmount(()=>{
//     if (socketIo) {
//       socketEmitter.removeListener('msgContent', this)
//       socketIo.close()
//     }
// })


// onMounted(()=>{
//     socketIo.open()//初始化打开链接 
//     socketEmitter.addListener('welcome', (data) => {//组件初始化挂载后，订阅后端事件
//       console.log('data', data)
//     }, this)
// })




// const socketOpen = () => {
//     $socketIo.open() 
// }


// const socketSendmsg = () => { // 发送消息
//       socketIo.emit('hello', '这里是客户端')
//     }

// const lockResult = () => {
//       console.log('链接状态', socketIo.connected)
//     }

// const closeSocket = () => {
//       socketIo.close()
//     }


// const  submsgContent = (flag) => {
//     if (flag) {
//         socketEmitter.addListener('welcome', (data) => {
//         console.log('data', data)
//     })
//     } else {
//         socketEmitter.removeListener('welcome')
//     } 
// }

</script> 