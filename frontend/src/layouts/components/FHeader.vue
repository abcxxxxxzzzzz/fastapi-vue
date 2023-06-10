<template>
    <div class="f-header">
        <span class="logo" :style="{ width:$store.state.asideWidth }" >
            <el-icon class="mr-1"><eleme-filled></eleme-filled></el-icon>
            <span v-if="$store.state.asideWidth =='250px'">Vue+Vite编程</span>
            <span v-else></span>
        </span>


        <el-icon class="icon-btn" @click="$store.commit('handleAsideWidth')">
            <fold v-if="$store.state.asideWidth =='250px'"/>
            <Expand v-else />
        </el-icon>

        <el-tooltip effect="dark" content="刷新" placement="bottom">
            <el-icon class="icon-btn" @click="handleRefresh"><refresh /></el-icon>
        </el-tooltip>
        


        <div class="ml-auto flex items-center">
            <el-tooltip effect="dark" content="全屏" placement="bottom">
                <el-icon  class="icon-btn" @click="toggle">
                    <full-screen v-if="!isFullscreen"/>
                    <aim v-else/>
                </el-icon>
            </el-tooltip>
            <el-dropdown class="dropdown" @command="handleCommand">
                <span class="flex items-center text-dark-900">
                    <img class="mr-2" height="30" width="30" style="border-radius: 50%;" src="@/assets/img/gw1L2Z5sPtS8GIl.gif" v-if="$store.state.user.avatar === null || $store.state.user.avatar ===''" />
                    <el-avatar class="mr-2" :size="25" :src="$store.state.user.avatar" v-else></el-avatar>

                    {{ $store.state.user.username }}
                    <el-icon class="el-icon--right"> <arrow-down /></el-icon>
                </span>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item command="rePassword">修改密码</el-dropdown-item>
                        <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                    </el-dropdown-menu>
                </template>
        </el-dropdown>
        </div>
    </div>


<!-- 修改密码 Start -->

    <form-drawer ref="formDrawerRef" title="修改密码" destroyOnClose @submit="onSubmit">

        <el-form  ref="formRef" :rules="rules" :model="form" label-width="80px" size="small">
            <el-form-item prop="oldpassword" label="旧密码">
                <el-input v-model="form.oldpassword" placeholder="请输入旧密码">
                    <template #prefix>
                        <el-icon><User /></el-icon>
                    </template>
                </el-input>
            </el-form-item>
            <el-form-item prop="password" label="新密码">
                <el-input type="password" v-model="form.password" placeholder="请输入新密码" show-password>
                    <template #prefix>
                        <el-icon><Lock /></el-icon>
                    </template>
                </el-input>
            </el-form-item>
            <el-form-item prop="repassword" label="确认密码">
                <el-input type="password" v-model="form.repassword" placeholder="请输入确认密码" show-password>
                    <template #prefix>
                        <el-icon><Lock /></el-icon>
                    </template>
                </el-input>
            </el-form-item>
        </el-form>

    </form-drawer>
    
<!-- 修改密码 End -->
</template>


<script setup>
import FormDrawer from '@/components/FormDrawer.vue'
import { useFullscreen } from '@vueuse/core'
import { userRepassword, useLogout } from '@/composables/useManager'




const { 
    // 是否全屏状态
    isFullscreen, 
    toggle 
} = useFullscreen()


const {
    formDrawerRef,
    form,
    rules,
    formRef,
    onSubmit,
    openRePasswordForm
} = userRepassword()


const {
    handleLogout
} = useLogout()


const handleCommand = (c) =>{
    switch (c) {
        case "logout":
            handleLogout()
            break;

        case "rePassword":
            openRePasswordForm()
            break;
    }
}


// 刷新
const handleRefresh = () => location.reload()


</script>

<style>
.f-header{
    background-color: #fff;
    @apply flex items-center  text-dark-900 fixed top-0 left-0 right-0;
    /* @apply flex items-center bg-indigo-500 text-light-50 fixed top-0 left-0 right-0; */
    height: 50px;
    z-index: 1000;
}

.logo{
    width: 250px;
    height: 100%;
    transition: all 0.2s;
    @apply flex justify-center items-center text-xl text-white font-thin bg-gray-800;
}

.icon-btn{
    @apply flex justify-center items-center;
    width: 42px;
    height: 50px;
    cursor: pointer;
}

.icon-btn:hover{
    @apply bg-indigo-600;
}

.f-header .dropdown{
    height: 50x;
    cursor: pointer;
    @apply flex justify-center items-center mx-5 ;
}
</style>