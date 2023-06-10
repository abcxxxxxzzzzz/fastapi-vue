<template>
    <div class="login-wrapper">
      <div class="login">
        <el-card class="login-center">
          <template #header>
            <div class="card_header">
              <span>6666</span>
            </div>
          </template>
          <el-form ref="loginFormRef" :model="loginFormState" :rules="loginRules">
                <el-form-item prop="username">
                <el-input
                    v-model.trim="loginFormState.username"
                    prefix-icon="el-icon-user-solid"
                    maxlength="100"
                    placeholder="请输入用户名"
                    clearable>

                    <template #prefix>
                      <el-icon><User /></el-icon>
                  </template>
                </el-input>
                </el-form-item>
                <el-form-item prop="password">
                <el-input
                    v-model.trim="loginFormState.password"
                    prefix-icon="el-icon-lock"
                    maxlength="100"
                    show-password
                    placeholder="请输入密码"
                    clearable
                    >

                    <template #prefix>
                        <el-icon><Lock /></el-icon>
                    </template>
                </el-input>
                </el-form-item>
                <el-form-item>
                <el-button type="primary" style="width: 100%" :loading="loginFormState.loading" @click="handleLogin">登录
                </el-button>
                </el-form-item>
          </el-form>
        </el-card>
      </div>
    </div>
  </template>
  
  <script setup>
import { ref, reactive, onMounted,onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { toast } from '@/utils/tools'
import store from '@/store'

const router = useRouter()

// do not use same name with ref
const loginFormState = reactive({
  username: '',
  password: '',
  
})

// 定义验证规则
const loginRules = {
    username: [
        {
            required: true,
            message: '用户名不能为空',
            trigger: 'blur',
        },
    ],
    password: [
        {
            required: true,
            message: '密码不能为空',
            trigger: 'blur',
        },
    ]
}

// 点击登录验证
const loginFormRef = ref(null)
const loading = ref(false)

const handleLogin = () => {
  loginFormRef.value.validate((valid) => {
        if (!valid) {
            console.log('error')
            return false;
        }
        // 加载按钮动画
        loading.value = true
        store.dispatch('login', loginFormState).then(res=>{
            toast('登录成功')
            router.push('/')

        }).finally(()=> {
            loading.value = false
        })
    })
}

// 监听回车事件
function onKeyUp(e){
    // console.log(e)
    if(e.key == 'Enter') handleLogin();
}

// 添加键盘添加
onMounted(()=>{
    document.addEventListener('keyup', onKeyUp)
})

// 移除键盘监听
onBeforeUnmount(()=>{
    document.removeEventListener('keyup', onKeyUp)
})
</script>

<style setup>

.login-wrapper {
  background: url('@/assets/img/login.jpg');
  background-size: 100% 100%;
}


.login {
  @apply min-w-screen min-h-screen flex justify-center items-center overflow-hidden;
}


.login .login-center {
  width: 396px;
  background-color: rgba(255, 255, 255,.1); 
  @apply h-auto border-none;
}

.login .card_header {
  color: #fff;
  @apply text-lg font-bold  text-center;
}

</style>