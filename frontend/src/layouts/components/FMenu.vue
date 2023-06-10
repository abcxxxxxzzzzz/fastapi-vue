<template>
    <div class="f-menu" :style="{ width:$store.state.asideWidth }">


        <el-menu unique-opened :collapse-transition="false"	:collapse="isCollapse" :default-active="defaultActive" class="border-0" @select="handleSelect">

        <template v-for="(item,index) in asideMenus" :key="index">
            <el-sub-menu v-if="item.children && item.children.length > 0" :index="item.name">
                <template #title>
                    <el-icon>
                        <component :is="item.icon"></component>
                    </el-icon>
                    <span>{{ item.name }}</span>
                </template>

                <el-menu-item v-for="(item2,index2) in item.children" :key="index2" :index="item2.frontpath">
                        <el-icon>
                            <component :is="item2.icon"></component>
                        </el-icon>
                        <span>{{ item2.name }}</span>
                </el-menu-item>
            </el-sub-menu>


            <el-sub-menu v-else :index="item.frontpath">
                    <el-icon>
                        <component :is="item.icon"></component>
                    </el-icon>
                    <span>{{ item.name }}</span>
            </el-sub-menu>
        </template>

        </el-menu>
</div>
</template>


<script setup> 
import { useRouter,useRoute,onBeforeRouteUpdate } from "vue-router"
import { computed,ref } from "vue";
import { useStore } from "vuex"

const router = useRouter()
const store = useStore()
const route = useRoute()


// 默认选中
const defaultActive = ref(route.path)

// 监听路由变化
onBeforeRouteUpdate((to,from)=>{
    defaultActive.value = to.path
})

// 是否折叠
const isCollapse = computed(()=> !(store.state.asideWidth == "250px"))

const asideMenus = computed(()=> store.state.menus)



const handleSelect = (e)=> {
    router.push(e)
}

</script>


<style setup>
.f-menu {
    /* width: 250px; */
    transition: all 0.2s;
    height: 100%;
    top: 50px;
    left: 0;
    /* overflow: auto; */
    overflow-y: auto;
    overflow-x: hidden;
    background-color: #304156;
    @apply shadow-md fixed;
    
}
.el-menu {
    background-color: #304156;
}


.el-sub-menu__title, .el-menu-item {
    color: #fafafa !important;
}


.el-menu-item.is-active {
    color: var(--el-menu-active-color) !important;
}


.f-menu::-webkit-scrollbar {
    widows: 0px;
}



.el-sub-menu__title:hover, .el-menu-item:hover {
    background-color: #646cff;
}
</style>