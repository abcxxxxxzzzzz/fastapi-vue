<template>
    <!-- <el-button text @click="dialogVisible = true">
      click to open the Dialog
    </el-button> -->
  
    <el-dialog
      v-model="dialogVisible"
      :title=title
      :width="size + '%'" 
      center
      align-center
      destroy-on-close
      draggable
    >
      <!-- <span>This is a message</span> -->

    <div class="body">
        <slot></slot>
    </div>


      <template #footer>
        <span class="dialog-footer">
          <el-button type="default" @click="close" >取消</el-button>
          <el-button type="primary" @click="submit" :loading="loading">
            确认
          </el-button>
        </span>
      </template>

    </el-dialog>


  </template>


<script  setup>
import { ref } from 'vue'

const dialogVisible = ref(false)
const open = ()=> dialogVisible.value = true  // 打开
const close = ()=> dialogVisible.value = false  // 关闭


const loading = ref(false)
const showLoading = ()=>loading.value = true
const hideLoading = ()=>loading.value = false


// 向父组件暴露方法
defineExpose({
        open,
        close,
        showLoading,
        hideLoading
})



const props = defineProps({
    title: String, 
    dialogVisible: Boolean,
    size: {
            // type: String,
            default: '30%'
        },
})


const emit = defineEmits(['submit'])
const submit = () => emit("submit")

</script>


<style scoped>
.dialog-footer button:first-child {
  margin-right: 10px;
}
</style>