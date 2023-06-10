<template>
    <el-container>
        <!-- <el-header>
            <f-header/>
        </el-header> -->
        <el-aside :width="$store.state.asideWidth">
                <f-menu/>
            </el-aside>
        <el-container>
            <!-- <el-aside :width="$store.state.asideWidth">
                <f-menu/>
            </el-aside> -->
            <el-header>
                <f-header/>
            </el-header>
            
            <el-main>
                <f-tag-list/>

                    <router-view v-slot="{ Component }">
                        <transition name="fade">
                            <keep-alive :max="10" v-if="$route.meta.keepAlive">
                                <component :is="Component"></component>
                            </keep-alive>
                            <keep-alive :max="10" v-else>
                                <component :is="Component"></component>
                            </keep-alive>

                        </transition>
                    </router-view>
            </el-main>
        </el-container>

    </el-container>
</template>


<script setup>
import FHeader from './components/FHeader.vue';
import FMenu from './components/FMenu.vue';
import FTagList from './components/FTagList.vue';
</script>


<style>
.el-aside {
    transition: all 0.2s;
}

.fade-enter-from{
    opacity: 0;
}

.fade-enter-to{
    opacity: 0;
}

.fade-leave-from{
    opacity: 1;
}

.fade-leave-to{
    opacity: 0;
}

.fade-enter-active,
.fade-leave-active{
    transition: all 0.3s;
}

.fade-enter-active {
    transition-delay: all 0.3s; 
}

</style>