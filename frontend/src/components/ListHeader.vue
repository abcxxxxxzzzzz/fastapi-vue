<template>
        <div class="flex items-center justify-between mb-4">
            <div>
                <el-button v-if="btns.includes('create')" type="primary" size="small" @click="$emit('create')"><el-icon><Plus /></el-icon>新增</el-button>

                <slot />

                <el-popconfirm
                    title="是否要删除该记录"
                    confirmButtonText="确认"
                    cancelButtonText="取消"
                    confirmButtonType="primary"
                    @confirm="$emit('delete')"
                    v-if="btns.includes('delete')"
                    >
                    <template #reference>
                        <el-button   type="danger" size="small">批量删除</el-button>
                    </template>
                </el-popconfirm>
                
            </div>

            
            <div>
                <!-- 刷新频率 -->
                <el-select v-model="count" v-if="Interval" class="m-2" placeholder="默认不刷新" size="small" fit-input-width clearable	style="width: 18vh;" @change="handleChangeSelect">
                    <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>

                <el-button v-if="btns.includes('download')" type="info" plain size="small"  @click="$emit('download')" ><el-icon><Download /></el-icon> 下载当页数据</el-button>
                <el-button v-if="btns.includes('condition')" type="info" plain size="small"  @click="$emit('condition')" ><el-icon><Download /></el-icon> 条件下载</el-button>
                            
                <el-tooltip v-if="btns.includes('refresh')"  content="刷新数据" placement="top" effect="dark">
                    <el-button type="primary" size="small"  @click="$emit('refresh')" text>
                        <el-icon :size="20"><Refresh /></el-icon>
                    </el-button>
                </el-tooltip>

            </div>
        </div>
</template>

<script setup>
import { computed,ref, onDeactivated } from 'vue';

const props = defineProps({
    layout: {
        type: String,
        default: "create,refresh"
    },
    Interval: {
        type: Boolean,
        default: false
    }
})

// 分割成数组
const btns = computed(()=>props.layout.split(','))

const emit =  defineEmits(['create','refresh','delete','download','condition'])




// 触发自动刷新按钮

const count = ref('')

const options = [
  {
    value: 3000,
    label: '3s 间隔自动刷新',
  },
  {
    value: 5000,
    label: '5s 间隔自动刷新',
  },
  {
    value: 10000,
    label: '10s 间隔自动刷新',
  },
  {
    value: 20000,
    label: '20s 间隔自动刷新',
  },
  {
    value: 30000,
    label: '30s 间隔自动刷新',
  },
  {
    value: 60000,
    label: '60s 间隔自动刷新',
  },
]

const timer = ref(null)



const handleChangeSelect = (val) => {
    clearInterval(timer.value);

    if (count.value == '') {
        clearInterval(timer.value);
    } else {
        timer.value = setInterval(() => {
            emit('refresh')
        },  count.value);
    }
}


// 退出触发清空, keep-alive组件缓存, 调用 onDeactivated
onDeactivated(() => {
    if (count.value != '') {
        count.value = ''
        clearInterval(timer.value);
    }
})



// beforeDestroy(() => {
    
//     clearInterval(timer.value);
// })

</script>