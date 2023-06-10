<template>
    <div class="f-tag-list" :style="{ left:$store.state.asideWidth }">

        <el-tabs
            v-model="activeTab"
            type="card"
            class="flex-1"
            @tab-remove="removeTab"
            style="min-width: 100px"
            @tab-change="changeTab"
        >
            <el-tab-pane
                :closable="item.path !='/'"
                v-for="item in tabList"
                :key="item.path"
                :label="item.title"
                :name="item.path"
                lazy
                >
            </el-tab-pane>
        </el-tabs>


        <!-- <el-tag
            :checked="activeTab"
            v-for="item in tabList"
            :key="item.path"
            class="mx-1"
            :closable="item.path !='/'"
            type="success"
            effect="dark"
            @close="removeTab"
            @click="changeTab"
        >
            {{ item.title }}
        </el-tag> -->


        <span class="tag-btn">
            <el-dropdown @command="handleClose">
                <span class="el-dropdown-link">
                <el-icon>
                    <arrow-down />
                </el-icon>
                </span>
                <template #dropdown>
                <el-dropdown-menu>
                    <el-dropdown-item command="clearOther">关闭其他</el-dropdown-item>
                    <el-dropdown-item command="clearAll">关闭全部</el-dropdown-item>
                </el-dropdown-menu>
                </template>
            </el-dropdown>
        </span>
    </div>

    <div style="height:44px;"></div>
</template>


<script setup>
import { useTabList } from '@/composables/useTabList'

const {
        activeTab,
        tabList,
        changeTab,
        removeTab,
        handleClose
    } = useTabList()
</script>

<style scoped>
.f-tag-list {
    @apply fixed bg-gray-100 flex items-center px-2;
    top: 50px;
    right: 0;
    height: 44px;
    z-index: 100;
    border: 1px solid var(--el-border-color-light);
    background-color: var(--el-bg-color);
    box-shadow: 0 1px 1px var(--el-box-shadow-light);
    transition: all 0.2s;
}

.tag-btn {
    @apply bg-white rounded ml-auto flex items-center justify-between px-1;
    height: 32px;
}


:deep(.el-tabs__header) {
    border: 0 !important;
    @apply mb-0;
}


:deep(.el-tabs__nav){
    border: 0 !important;
}

:deep(.el-tabs__item){
    /* border: 0 !important; */
    /* @apply bg-white mx-1 rounded; */
    display: inline-block;
    cursor: pointer;
    border-top: 1px  solid var(--el-border-color-light);
    border-right: 1px  solid var(--el-border-color-light);
    border-left: 1px  solid var(--el-border-color-light);
    padding: 1px 15px;
    font-size: 12px;
    font-weight: 700;
    margin: 0px 5px 0px 5px;
    border-bottom: 0 !important;
}

:deep(.el-tabs__nav-next),:deep(.el-tabs__nav-prev){
    line-height: 32px;
    height: 32px;
}

:deep(.is-disabled){
    cursor: not-allowed;
    @apply text-gray-300;
}
</style>