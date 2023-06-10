<template>
    <el-card shadow="always" class="border-0">

            <!-- 搜索 -->
            <Search @model="searchForm" @search="getData" @reset="resetSearchFrom">

                <SearchItem label="词汇来源">
                    <el-select v-model="searchForm.type"  placeholder="" clearable filterable v-permission="['getListKeyWord,GET']" >
                        <el-option v-for="(item, index)  in keywordType"
                            :key="item.type"
                            :label="item.type"
                            :value="item.type"
                            >
                        </el-option>
                    </el-select>
                </SearchItem>

                
                <SearchItem label="关键词">
                        <el-input
                            placeholder="模糊搜索"
                            v-model="searchForm.keyword"
                            @keyup.enter="getData"
                            v-on:input="getData"
                            >
                        </el-input>
                </SearchItem>









    
                <!-- 添加到自定义插槽 -->
                <template #show>


                    <SearchItem label="查询状态">
                        <el-select v-model="searchForm.status"  placeholder="" clearable filterable>
                            <el-option v-for="(item, index)  in keywordStatus"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                                >
                            </el-option>
                        </el-select>
                    </SearchItem>

                    <SearchItem label="创建时间">
                    <el-date-picker
                        v-model="searchForm.start_end"
                        type="datetimerange"
                        unlink-panels
                        range-separator="到"
                        start-placeholder="开始时间"
                        end-placeholder="结束时间"
                        :shortcuts="shortcuts"
                        size="small"
                        format="YYYY-MM-DD HH:mm:ss"
                        value-format="YYYY-MM-DD HH:mm:ss"
                        :default-time="defaultTime"
                    />


                </SearchItem>

                <SearchItem label="更新时间">
                    <el-date-picker
                        v-model="searchForm.update_start_end"
                        type="datetimerange"
                        unlink-panels
                        range-separator="到"
                        start-placeholder="开始时间"
                        end-placeholder="结束时间"
                        :shortcuts="shortcuts"
                        size="small"
                        format="YYYY-MM-DD HH:mm:ss"
                        value-format="YYYY-MM-DD HH:mm:ss"
                        :default-time="defaultTime"
                    />


                </SearchItem>
                    
                </template>
            </Search>


            <el-progress
                :text-inside="true"
                :stroke-width="20"
                :percentage="percentageValue"
                :color="colors"
                class="mb-6"
                v-show="percentageValue != null"
                >
            
                <template #default="{ percentage  }">
                    <span class="percentage-label">{{ percentageLabel }}</span>
                    <span class="percentage-value">{{ percentageValue }}%</span>
                    
                </template>
            </el-progress>

        <!-- 表格头部 --> 
        <ListHeader layout="refresh,download,condition" @download="exportToExcel" @condition="conditionToExcel" @refresh="getData" >
            <el-button type="primary"  plain size="small" @click="handleCreate" v-permission="['createKeyWord,POST']"><el-icon><Plus /></el-icon>新增</el-button>
            <el-button type="warning"  plain size="small" @click="handleBatchAdd"  v-permission="['batchAddKeyWord,POST']"><el-icon><Plus /></el-icon>批量添加</el-button>
            <el-button color="#626aef"  plain size="small" @click="handleBatchUpdata"  v-permission="['batchUpdataKeyWord,POST']"><el-icon><EditPen /></el-icon>选中更新</el-button>
            <el-button color="#c30eb3"  plain size="small" @click="conditionUpdate"  v-permission="['ConditionBatchUpdateKeyword,POST']"><el-icon><EditPen /></el-icon>条件更新</el-button>


            <el-popconfirm
                title="是否要批量彻底删除选择的记录,不可逆操作"
                confirmButtonText="确认"
                cancelButtonText="取消"
                confirmButtonType="primary"
                @confirm="handleMultiDelete">
                <template #reference>
                    <el-button type="danger" size="small" v-permission="['batchDeleteKeyWord,POST']" plain><el-icon><Delete /></el-icon> 批量删除</el-button>
                </template>
            </el-popconfirm>


        </ListHeader>

        <!-- 表格 -->
        <el-table :data="tableData" @selection-change="handleSelectionChange" header-align="center" style="width: 100%; font-size: 1vh;"  v-loading="loading" v-permission="['getListKeyWord,GET']"  border>
            <el-table-column fixed type="selection" width="55"/>
            <el-table-column prop="type" label="词汇来源" align="center" width="80"></el-table-column>
            <el-table-column prop="name" label="关键词" align="center" width="250">
                <template  #default="{ row }">
                    <span>{{ row.name }}</span>
                    <el-button text size="small" circle @click="copy(row)" ><el-icon ><CopyDocument /></el-icon></el-button>
                </template>
            </el-table-column>
            <el-table-column prop="status" label="查询状态" align="center" >
                <template  #default="{ row }">
                    <el-tag class="ml-2"
                    :type="row.status == -2 ? 'info' : row.status == -1 ?  'warning' : row.status == 1 ? 'success': 'info'"
                    >
                        {{ row.status == -2 ? '未查询' : row.status == -1 ?  '正在查询' : row.status == 1 ? '已查询': '未知'}}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="name" label="已汇总数量" align="center" >
                <template  #default="{ row }">
                    <span>{{ row.searchkeywords ? row.searchkeywords.length : 0 }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="search_user" label="分配者"  align="center"   />
            <el-table-column prop="first_name" label="创建者"  align="center"   />
            <el-table-column prop="last_name" label="更新者"   align="center"   />
            
            <el-table-column prop="created_at" label="创建时间" align="center"  width="150">
                <template  #default="{ row }">
                    <span>{{ row.created_at ? dateFormat(row.created_at) : '' }}</span>
                </template>
            </el-table-column>

            <el-table-column prop="created_at" label="更新时间"  align="center" width="150">
                <template  #default="{ row }">
                    <span>{{ row.updated_at ? dateFormat(row.updated_at) : ''  }}</span>
                </template>
            </el-table-column>


            <el-table-column label="操作" fixed="right"  align="center" width="110">
                <template #default="scope">

                    <el-button 
                        size="small" 
                        :icon="Edit"
                        @click="handleEdit(scope.row)"
                        v-permission="['modifyKeyWord,PUT']"
                    /> 

                    <el-popconfirm
                        title="是否要删除该记录"
                        confirmButtonText="确认"
                        cancelButtonText="取消"
                        confirmButtonType="primary"
                        @confirm="handleDelete(scope.row.id)"
                        >
                        <template #reference v-permission="['deleteKeyWord,DELETE']">
                            <el-button size="small" :icon="Delete" type="danger" />
                        </template>
                    </el-popconfirm>
                </template>
            </el-table-column>
        </el-table> 
        <!-- 分页 -->  
        <div class="flex items-center justify-center mt-5">
                <el-pagination
                    v-model:current-page="searchForm.skip"
                    v-model:page-size="searchForm.limit"
                    :page-sizes="[10, 50, 100, 300, 500, 1000]"
                    small="small"
                    background="background"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="total"
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                />
        </div>
        

        <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit">
            <el-form :model="form" ref="formRef" :rules="rules" label-width="80px">
                <el-form-item label="关键词" prop="name">
                    <el-input v-model="form.name"  placeholder="关键词名称" size="small"></el-input>
                </el-form-item>

                <el-form-item label="查询状态" prop="status">
                    <el-select v-model="form.status" size="small" style="width: 100%" placeholder="" clearable filterable>
                        <el-option v-for="(item, index)  in keywordStatus"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                            >
                        </el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="词汇来源">
                    <el-radio-group v-model="radioType" class="ml-2"  @change="handleRadioType">
                        <el-radio label="1" size="small" border>已有来源</el-radio>
                        <el-radio label="2" size="small" border>添加来源</el-radio>
                    </el-radio-group>
                </el-form-item>


                <el-form-item label="已有来源" prop="type" v-if="radioType == 1">
                    <el-select v-model="form.type" style="width: 100%" placeholder="" size="small" clearable filterable >
                        <el-option v-for="(item, index)  in keywordType"
                            :key="item.type"
                            :label="item.type"
                            :value="item.type"
                            >
                        </el-option>
                    </el-select>
                </el-form-item>


                <el-form-item label="添加来源" prop="type" v-if="radioType == 2">
                    <el-input v-model="form.type"  placeholder="添加新的词汇来源,例如： 百度" size="small"></el-input>
                </el-form-item>


            </el-form>


                        
        </FormDrawer>


            <!-- 批量搜索 || 批量更新 -->
            <el-drawer :title="batchAddTitle" ref="formAddDrawerRef" v-model="batchAddDrawer" >
                

                <div class="formDrawer">
                    <div class="body">
                        <el-form :model="batchAddForm" ref="formBatchAddRef" :rules="batchAddRules" label-width="80px">
                            <el-form-item label="添加内容" prop="batchContent">
                                <el-input v-model="batchAddForm.batchContent" type="textarea" :rows="20" placeholder="添加的内容，一行一个"></el-input>
                            </el-form-item>


                            <el-form-item label="词汇来源">
                                <el-radio-group v-model="radioType" class="ml-2"  @change="handleRadioType">
                                    <el-radio label="1" size="small" border>已有来源</el-radio>
                                    <el-radio label="2" size="small" border>添加来源</el-radio>
                                </el-radio-group>
                            </el-form-item>


                            <el-form-item label="已有来源" prop="type" v-if="radioType == 1">
                                <el-select v-model="batchAddForm.type" style="width: 100%" placeholder="" size="small" clearable filterable >
                                    <el-option v-for="(item, index)  in keywordType"
                                        :key="item.type"
                                        :label="item.type"
                                        :value="item.type"
                                        >
                                    </el-option>
                                </el-select>
                            </el-form-item>


                            <el-form-item label="添加来源" prop="type" v-if="radioType == 2">
                                <el-input v-model="batchAddForm.type"  placeholder="添加新的词汇来源,例如： 百度" size="small"></el-input>
                            </el-form-item>

                        </el-form>
                    </div>
                    <div class="actions">
                        <el-button type="primary" :loading="loading" @click="batchAddsubmit">确定</el-button>
                        <el-button type="default"  @click="batchAddclose">取消</el-button>
                    </div>
                </div>
            </el-drawer>
    






        <!-- 条件下载模态框 -->
        <FormDialog :title='DialogTitle'  ref="formTjDialogRef" @submit="dialogSubmit">
            <el-descriptions
                title="下载到 EXCEL 条件内容"
                :column="1"
                size="small"
                border
            >
                <el-descriptions-item label="关键词">{{ searchForm.type }}</el-descriptions-item>
                <el-descriptions-item label="关键词">{{ searchForm.keyword }}</el-descriptions-item>
                <el-descriptions-item label="是否查询">
                    <span v-if="searchForm.status == -2">未查询</span>
                    <span v-else-if="searchForm.status == -1">正在查询</span>
                    <span v-else-if="searchForm.status == 1">已查询</span>
                    <span v-else></span>

                </el-descriptions-item>
 
                <el-descriptions-item label="创建时间">{{ searchForm.start_end ? searchForm.start_end.join('~') : '' }}</el-descriptions-item>
                <el-descriptions-item label="更新时间">{{ searchForm.update_start_end ? searchForm.update_start_end.join('~'): '' }}</el-descriptions-item>

                <el-descriptions-item label="默认">
                    <el-tag size="small" type="danger">如果以上无数据, 没有条件, 则下载所有,否则下载符合相关条件数据</el-tag>
                </el-descriptions-item>
            </el-descriptions>
        </FormDialog>



        <!-- 批量添加重复提示 -->
        <el-dialog :title='existKeyWordTitle'  ref="formDialogRef" v-model="existKeyWordDrawer">
            <span>批量添加成功: <span style="color:green">{{ successTotal }}</span>; </span><span>批量添加失败: <span style="color: red;">{{ errorTotal  }}</span></span>
            
            <el-divider />

            <div>
                <p v-for="item in errorData" :key="item">{{ item }}</p>
            </div>

        </el-dialog>



        <!-- 批量更新 -->
        <FormDialog :title='UpdataDialogTitle'  ref="UpdataDialogRef" @size="5" @submit="UpdataDialogSubmit">
            <div class="body">
                <el-form :model="UpdatabatchForm" ref="UpdataFormBatchRef" :rules="UpdatabatchRules">
                    <el-form-item label="" prop="status">
                            <el-select v-model="UpdatabatchForm.status"  placeholder="" clearable filterable>
                                <el-option v-for="(item, index)  in keywordStatus"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value"
                                    >
                                </el-option>
                            </el-select>                    
                    </el-form-item>
                </el-form>
            </div>
        </FormDialog>


                <!-- 条件更新 -->
        <FormDialog :title='ConditionUpdateChildDialogTitle'  ref="ConditionUpdataChildDialogRef" @size="5" @submit="ConditionUpdateChildDialogSubmit">
            <div class="body">
                <el-form :model="ConditionUpdateChildForm" ref="ConditionUpdateChildFormRef" :rules="ConditionUpdataChildRules">
                    <el-form-item label="" prop="status">
                            <el-select v-model="ConditionUpdateChildForm.status"  placeholder="" clearable filterable>
                                <el-option v-for="(item, index)  in keywordStatus"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value"
                                    >
                                </el-option>
                            </el-select>                    
                    </el-form-item>
                </el-form>
            </div>
        </FormDialog>


        
        <!-- 条件更新模态框 -->
        <FormDialog :title='ConditionUpdateDialogTitle'  ref="ConditionUpdateDialogRef" @submit="updateConditionDialogSubmit">
            <el-descriptions
                :column="1"
                size="small"
                border
            >
                <el-descriptions-item label="关键词">{{ searchForm.type }}</el-descriptions-item>
                <el-descriptions-item label="关键词">{{ searchForm.keyword }}</el-descriptions-item>
                <el-descriptions-item label="是否查询">
                    <span v-if="searchForm.status == -2">未查询</span>
                    <span v-else-if="searchForm.status == -1">正在查询</span>
                    <span v-else-if="searchForm.status == 1">已查询</span>
                    <span v-else></span>

                </el-descriptions-item>
 
                <el-descriptions-item label="创建时间">{{ searchForm.start_end ? searchForm.start_end.join('~') : '' }}</el-descriptions-item>
                <el-descriptions-item label="更新时间">{{ searchForm.update_start_end ? searchForm.update_start_end.join('~'): '' }}</el-descriptions-item>

                <el-descriptions-item label="默认">
                    <el-tag size="small" type="danger">如果以上无数据, 没有条件, 则{{ConditionUpdateDialogTitle}}所有,否则{{ConditionUpdateDialogTitle}}符合相关条件数据</el-tag>
                </el-descriptions-item>
            </el-descriptions>
        </FormDialog>


        <!-- 点击下载完成后提示框 -->
        <el-dialog :title='downloadTitle'  ref="formDialogRef" v-model="downloadDialog">
            
            <el-divider />
            <h3>
                <a :href="'api/' + downloadPath" style="color: green;"  >点击下载</a>
            </h3>
            <el-divider />
        </el-dialog>

    </el-card>


    

    
</template>


<script setup>
import { ref,reactive,onMounted,watchEffect,onDeactivated } from 'vue'
import { Delete, Edit } from '@element-plus/icons-vue'
import Search from '@/components/Search.vue'
import SearchItem from '@/components/SearchItem.vue'
import { toast, getNextDate,getCurrentTime } from '@/utils/tools.js'

import { 
    getKeyWordType,
    getKeyWordList,
    createKeyWord,
    updateKeyWord,
    deleteKeyWord,
    batchCreateKeyWord,
    batchDeleteKeyWord,
    batchUpdataKeyWord,
    ConditionBatchUpdateKeyword,
    getTaskProgress
    
} from "@/api/keyword.js"
import ListHeader from '@/components/ListHeader.vue';
import FormDrawer from '@/components/FormDrawer.vue';
import FormDialog from '@/components/FormDialog.vue'
import { useInitTable,useInitForm } from '@/composables/useCommon'
import { dateFormat } from '@/utils/tools.js'
import useClipboard from "vue-clipboard3"
import { exportExcel } from '@/utils/exportExcel'


const keywordStatus = ref([])
const keywordType = ref([])


const radioType =  ref('1')

const {
    searchForm,
    resetSearchFrom,
    tableData,
    loading,
    // currentPage,
    total,
    // limit,
    getData,
    handleDelete,
    handleMultiDelete,
    handleSelectionChange,
    multiSelectionIds
    // handleStatusChange
} = useInitTable({
    searchForm: {
        keyword: '',
        status: '',
        skip: 1,
        limit: 10,
        start_end: '',
        update_start_end: '',
        paging: 1,
        type: ''
    },
    rules: {
        name: [{
                required: true,
                message: '关键词名称不能为空',
                trigger: 'blur',
            },],
},
    onGetListSuccess: (res)=> {
                tableData.value = res.list.map(o=>{
                    o.statusLoading = false
                    return o
                })

                total.value = res.totalCount
                keywordStatus.value = res.keywordStatus
                

        },
    getList: getKeyWordList,
    delete: deleteKeyWord,
    multidelete: batchDeleteKeyWord,
})


const {
    formDrawerRef,
    formRef,
    form,
    rules,
    drawerTitle,
    handleSubmit,
    handleCreate,
    handleEdit
} = useInitForm({
    form: {
        name:'',
        status: '',
        type: '',
    },
    rules: {
        name: [{
                required: true,
                message: '关键词名称不能为空',
                trigger: 'blur',
            },],
        status: [{
                required: true,
                message: '查询状态不能为空',
                trigger: 'blur',
            },],
        type: [{
                required: true,
                message: '词汇来源不能为空',
                trigger: 'blur',
            },],
    },


    getData,
    update: updateKeyWord,
    create: createKeyWord
})


const handleSizeChange = (val) => {
  getData()
}
const handleCurrentChange = (val) => {
  getData()
}


const handleRadioType = (val) => {
    console.log(val)
}

onMounted(()=> {
    // keywordType.value = ['百度','搜狗']
    setTimeout(() => {
        getKeyWordType().then(res=> {
            keywordType.value = res.keywordType
        })
    }, 100)
})




// 批量添加 
const successTotal = ref(0)
const errorTotal = ref(0)
const errorData = ref([])
const existKeyWordTitle = ref(null)
const existKeyWordDrawer = ref(false)

const formBatchAddRef = ref(null)
const batchAddDrawer = ref(false)
const batchAddTitle = ref(null)
const batchAddForm = reactive({
    batchContent: '',
    type: '',
})
const batchAddRules = {
    batchContent: [
            {
                required: true,
                message: '内容不能为空',
                trigger: 'blur',
            },
        ],
    type: [
            {
                required: true,
                message: '词汇来源不能为空',
                trigger: 'blur',
            },
        ],
}


const  handleBatchAdd = () => {
    batchAddTitle.value = '批量添加'
    batchAddDrawer.value = true
}

const batchAddsubmit = () => {
    formBatchAddRef.value.validate((valid)=>{
        if(!valid) return false

        loading.value = true

    
        batchCreateKeyWord(batchAddForm).then(res=>{
            toast(batchAddTitle.value + '成功')
            formBatchAddRef.value.resetFields()
            batchAddDrawer.value = false

            // 如果存在数据，则打开对话框
            if(res.errorTotal > 0) {
                existKeyWordDrawer.value = true
                existKeyWordTitle.value = '已存在的数据'
                successTotal.value = res.successTotal
                errorTotal.value = res.errorTotal
                errorData.value = res.errorData
            }
            getData()
        }).finally(()=>{
            loading.value = false
        })

    })

}
const batchAddclose = () => batchAddDrawer.value = false







// 复制
const { toClipboard } = useClipboard();
    const copy = async (row) => {
    try {
        await toClipboard(row.name);
        // toast('归属系列:'+ row.owner.name + '\n' +'下的渠道号:'+ row.channel_code + 'OP链接复制成功:');
        toast('<p>关键词名称: '+ row.name + '</p><p style="margin-top: 10px;color: green;">复制成功</p>');

    } catch (e) {
        toast('复制失败 || 关键词名称不存在','warning')
        console.error(e);
    }
};




// 搜索日期选择
// const keywordDate = ref('')
// const defaultTime = new Date(2000, 1, 1, 0, 0, 0) // '12:00:00'
const defaultTime =  ref([
  new Date(2000, 1, 1, 12, 0, 0),
  new Date(2000, 2, 1, 8, 0, 0),
])

const date = new Date()
const current_day = date.getDate();  // 日
const current_month = date.getMonth() + 1
const current_year = date.getFullYear()


const shortcuts = [
    {
        text: '今天',
        value: () => {
            const _startDay = current_year + '-' + current_month + '-' + current_day
            const startDay = getNextDate(_startDay, 0)
            const end = date.setTime(date.getTime())
            return [startDay, end]
        },
    },
    {
        text: '昨天',
        value: () => {
            const endDay = current_year + '-' + current_month + '-' + current_day
            const startDay = getNextDate(endDay, -1)
            return [startDay, endDay]
        },
    },
    {
        text: '前天',
        value: () => {
            const endDay = current_year + '-' + current_month + '-' + current_day
            const startDay = getNextDate(endDay, -2)
            const _endDay = getNextDate(endDay, -1)
            return [startDay, _endDay]
        },
    },
    {
        text: '最近三天',
        value: () => {
            const end = new Date()
            const start = new Date()

            start.setTime(start.getTime() - 3600 * 1000 * 24 * 3)
            return [start, end]
        },
    },
    {
        text: '最近七天',
        value: () => {
            const end = new Date()
            const start = new Date()

            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
            return [start, end]
        },
    },
    {
        text: '最近一个月',
        value: () => {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
            return [start, end]
        },
    },
    {
        text: '最近三个月',
        value: () => {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
            return [start, end]
        },
    },

    {
        text: '最近六个月',
        value: () => {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 180)
            return [start, end]
        },
    },

]





function fieldReplace(newDate) {
    newDate.forEach(e => {
        if(e.status == -2) {
            e.status = "未查询"
        } else if (e.status == -1) {
            e.status = "正在查询"
        } else if(e.status == 1) {
            e.status = "已查询"
        } else {
            e.status = '未知'
        }
    });

    return newDate
}

// 下载当页数据
const exportToExcel = ()=> {
    
    loading.value = true

    let newDate = fieldReplace(tableData.value)
    
    let fields = {
        name: "关键词名称",
        status: "查询状态",
    };


    // let data = JSON.parse(JSON.stringify(this.tableData3));  // 如果直接放置数据不行请加上这句

    exportExcel(newDate, fields, getCurrentTime() + "_关键词管理");
    getData()

    loading.value = false
}







// 条件下载
const formTjDialogRef = ref(null)
const DialogTitle = ref(null)
const conditionToExcel = () => {
    DialogTitle.value = '条件下载确认'
    formTjDialogRef.value.open()
}


const dialogSubmit = () => {

    // 条件标识及加载
    formTjDialogRef.value.showLoading()
    searchForm.paging = 0
    loading.value = true

    // 从后端获取数据
    getKeyWordList(searchForm).then(async res => {
        task_id.value = res.task_id
        percentageLabel.value = '条件下载任务进度 '
        toast('条件下载任务已添加，正在执行，请不要关闭页面，注意观察进度条情况，请耐心等等')
        timerLoading.value = setInterval(() => {
            doIntervalDonwLoad()   
        }, 5000);

        formTjDialogRef.value.close()
    }) .finally(()=>{
        loading.value = false
        formTjDialogRef.value.hideLoading()
        resetSearchFrom()
    })
} 



// 批量选中更新
const UpdataDialogRef = ref(false)
const UpdataDialogTitle = ref(null)
const UpdataFormBatchRef = ref(null)
const UpdatabatchForm = reactive({
    ids: [],
    status: ''
})

const UpdatabatchRules = {
    status: [
        {
            required: true,
            message: '更新内容不能为空',
            trigger: 'blur',
        },
    ]
}



const handleBatchUpdata = () => {
    if(multiSelectionIds.value.length == 0) {
        toast('请先选择需要更新的数据', 'warning')
        return false
    }

    UpdataDialogTitle.value = '选中更新'
    UpdataDialogRef.value.open()
    

}


const UpdataDialogSubmit = () => {
    
    UpdatabatchForm.ids = multiSelectionIds.value
    UpdataFormBatchRef.value.validate((valid) => {
        if (!valid) {
            console.log('error',valid)
            return false;
        }

        UpdataDialogRef.value.showLoading()
        batchUpdataKeyWord(UpdatabatchForm)
        .then(res=> {
            toast('修改成功')
            UpdataFormBatchRef.value.resetFields()
            UpdataDialogRef.value.close()
            
            getData()
        }).finally(()=>{
            UpdataDialogRef.value.hideLoading()
            
        })
    })
} 




// 条件更新
const ConditionUpdateDialogRef = ref(false)
const ConditionUpdateDialogTitle = ref(null)

const ConditionUpdateChildDialogTitle = ref(null)
const ConditionUpdataChildDialogRef = ref(false)
const ConditionUpdateChildFormRef = ref(null)
const ConditionUpdateChildForm = reactive({
    status: ''
})

const ConditionUpdataChildRules = {
    status: [
        {
            required: true,
            message: '更新内容不能为空',
            trigger: 'blur',
        },
    ]
}

const conditionUpdate = () => {
    ConditionUpdateDialogTitle.value = '条件更新'
    ConditionUpdateDialogRef.value.open()
}


const updateConditionDialogSubmit = () => {
    ConditionUpdateChildDialogTitle.value = "请选中更新条件"
    ConditionUpdataChildDialogRef.value.open()
}



const ConditionUpdateChildDialogSubmit = () => {

    ConditionUpdateChildFormRef.value.validate((valid) => {
        if (!valid) {
            console.log('error',valid)
            return false;
        }
        loading.value = true
        ConditionUpdateDialogRef.value.showLoading()
        ConditionUpdataChildDialogRef.value.showLoading()
        ConditionBatchUpdateKeyword(searchForm, ConditionUpdateChildForm).then(async res=> {

            toast('条件更新成功')
            getData()
            
            ConditionUpdataChildDialogRef.value.close()
            ConditionUpdateDialogRef.value.close()
            
        }).finally(() => {
            loading.value = false
            ConditionUpdateDialogRef.value.hideLoading()
            ConditionUpdataChildDialogRef.value.hideLoading()
        })

    })
}

// 进度条
const task_id = ref(null)
const timerLoading = ref(null)
const colors = [
  { color: '#f56c6c', percentage: 20 },
  { color: '#e6a23c', percentage: 40 },
  { color: '#5cb87a', percentage: 60 },
  { color: '#1989fa', percentage: 80 },
  { color: '#6f7ad3', percentage: 100 },
]

const percentageLabel = ref(null)
const percentageValue = ref(null)
watchEffect(() => {
    // percentageLabel.value = '文件上传任务进度 '
    if(percentageValue.value == 100) {
        setTimeout(()=>{
            percentageValue.value = null
            clearInterval(timerLoading.value)
        },1000)
    }

    
})

// 循环获取下载数据定时器
const downloadTitle = ref(null)
const downloadDialog = ref(false)
const downloadPath = ref(null)
function doIntervalDonwLoad() {
    // percentageValue.value = null
    getTaskProgress({'task_id': task_id.value}).then(res => {
            let num = parseInt(res.task.progress)

            

            if (num >= 100) {
                percentageValue.value = null
                task_id.value = ''
                clearInterval(timerLoading.value)
                // 并展示出来
                toast("条件下载数据完成")
                console.log("地址：", res)
                downloadPath.value = res.task.description
                downloadTitle.value = '条件下载数据信息提示'

                setTimeout(()=> {
                    downloadDialog.value = true
                },1000)

            } 
            percentageValue.value = num
        })
}



onDeactivated(() => {
    clearInterval(timerLoading.value);
    percentageValue.value = null
})

</script>


