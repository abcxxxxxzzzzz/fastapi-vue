<template>
    <el-upload
        class="upload-demo"
        drag
        :action="action"
        :multiple="multiple"
        :headers="{
          'X-Token': token
        }"
        name="img"
        :data="data"
        :on-success="uploadSuccess"
        :on-error="uploadError"
        >
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>

      <div class="el-upload__text">
        拖动图片到这里 或<em>点击上传</em>
      </div>

      <template #tip>
        <div class="el-upload__tip">
          jpg/png 文件大小不超过 500kb
        </div>
      </template>
    </el-upload>
</template>
  
<script setup>
// import { uploadImageAction } from "@/api/image"
import { getToken } from "@/utils/cookies"
import { toast } from '@/utils/tools'

const token = getToken()
const emit = defineEmits(['success'])

const uploadSuccess =(response, uploadFile, uploadFiles)=>{
  toast('上传成功')
  emit('success',{
    response, uploadFile, uploadFiles
  })
}

const uploadError =(error, uploadFile, uploadFiles)=>{
  let msg = JSON.parse(error.message).msg || "上传失败"
  toast(msg,"error")
}


defineProps({
  data: Object,
  action: String,
  multiple: {
    default: false,
    String
  }
})
</script>
  