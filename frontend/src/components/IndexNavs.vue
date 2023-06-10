<template>
    <el-row :gutter="20" class="mt-5">
        <el-col :span="3" :offset="0" v-for="(item,index) in iconNavs" :key="index">
            <el-card shadow="hover" @click="$router.push(item.path)">
                <div class="flex  flex-col items-center justify-center cursor-pointer">
                    <el-icon :size="16" :class="item.color">
                        <component :is="item.icon"></component>
                    </el-icon>
                    <span class="text-sm mt-2">{{ item.title }}</span>
                </div>
            </el-card>
        </el-col>
    </el-row>
    
</template>


<script setup>

const iconNavs = [
    {
        icon: "user",
        color: "text-light-blue-500",
        title: "用户",
        path: "/admin/users"
    },
    {
        icon: "shopping-cart",
        color: "text-violet-500",
        title: "部门",
        path: "/admin/groups"
    },
    {
        icon: "tickets",
        color: "text-fuchsia-500",
        title: "角色",
        path: "/admin/roles"
    },
    {
        icon: "picture",
        color: "text-rose-500",
        title: "权限",
        path: "/admin/permissions"
    },
]
</script>