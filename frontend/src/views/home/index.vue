<template>
    <div>
        <el-row :gutter="20" v-permission="['getStatistics,GET']">

            <!-- 骨架屏优化体验 -->
            <template v-if="panels.length == 0">
                <el-col :span="6" :offset="0" v-for="i in 4" :key="i">
                <el-skeleton style="width: 100%;" animated loading>
                    <template #template>
                        <el-card shadow="hover" class="border-0">
                            <template #header>
                                <div class="flex justify-between">
                                    <el-skeleton-item variant="text" style="width: 50%" />
                                    <el-skeleton-item variant="text" style="width: 10%" />

                                </div>
                            </template>

                            <el-skeleton-item variant="text" style="width: 80%" />
                            <el-divider></el-divider>
                            <div class="flex justify-between text-sm text-gray-500">
                                <el-skeleton-item variant="text" style="width: 50%" />
                                <el-skeleton-item variant="text" style="width: 10%" />
                            </div>


                        </el-card>

                        <el-skeleton-item variant="text" style="width: 30%" />
                    </template>
                </el-skeleton>
            </el-col>
            </template>

            <!--  -->
            <el-col :span="6" :offset="0" v-for="(item, index) in panels" :key="index" >
                <el-card shadow="hover" class="border-0">
                    <template #header>
                        <div class="flex justify-between">
                            <span>{{ item.title }}</span>
                            <el-tag :type="item.unitColor" effect="plain">
                                {{ item.unit }}
                            </el-tag>

                        </div>
                    </template>

                    <span class="text-3xl font-bold text-gray-500">
                        <!-- {{ item.value }} -->
                        <CountTo :value="item.value"/>
                    </span>
                    <el-divider></el-divider>
                    <div class="flex justify-between text-sm text-gray-500">
                        <span>{{ item.subTitle }}</span>
                        <span>{{ item.subValue }}</span>
                    </div>
                </el-card>

            </el-col>
        </el-row>

        <!-- 分类组件 -->
        <IndexNavs></IndexNavs>

        

</div>
</template>

<script setup>
import { getStatistics } from '@/api/index';
import { ref } from 'vue';
import CountTo from   '@/components/CountTo.vue';
import IndexNavs from '@/components/IndexNavs.vue';



const panels = ref([])
getStatistics().then(res => {
    console.log(res.panels)
    panels.value = res.panels
})

</script>