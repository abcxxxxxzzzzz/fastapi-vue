<template>
    <el-card shadow="always" class="border-0">

            <!-- 搜索 -->
            <Search @model="searchForm" @search="getData" @reset="resetSearchFrom">
                <SearchItem label="权重域名">
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


                    <SearchItem label="权重类别">
                        <el-select v-model="searchForm.type"  placeholder="" clearable filterable>
                            <el-option v-for="(item, index)  in weightTypes"
                                :key="item"
                                :label="item"
                                :value="item"
                                >
                            </el-option>
                        </el-select>
                    </SearchItem>


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


                

                    <SearchItem label="域名类型">
                        <el-select v-model="searchForm.en"  placeholder="" clearable filterable>
                            <el-option v-for="(item, index)  in ens"
                                :key="item"
                                :label="item"
                                :value="item"
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
        <ListHeader  layout="refresh,download,condition" @refresh="getData" @condition="conditionToExcel" @download="exportToExcel">
            <el-button type="primary" plain size="small" @click="handleCreate" v-permission="['createWeight,POST']"><el-icon><Plus /></el-icon>新增</el-button>
            <el-button type="warning" plain size="small" @click="handleBatchAdd"  v-permission="['batchAddWeight,POST']"><el-icon><Plus /></el-icon>批量添加</el-button>
            <el-button color="#626aef"  plain size="small" @click="handleBatchUpdata"  v-permission="['batchUpdataWeight,POST']"><el-icon><EditPen /></el-icon>选中更新</el-button>
            <el-button color="#c30eb3"  plain size="small" @click="conditionUpdate"  v-permission="['ConditionBatchUpdateWeigh,POST']"><el-icon><EditPen /></el-icon>条件更新</el-button>
            <!-- <el-button color="#c30eb3"  plain size="small" @click="conditionUpdate"><el-icon><EditPen /></el-icon>条件更新</el-button> -->

            <!-- <el-button type="warning" plain size="small" @click="handleBatchAdd"  v-permission="['batchAddWeight,POST']"><el-icon><Plus /></el-icon>批量添加</el-button> -->


            <el-popconfirm
                title="是否要批量彻底删除选择的记录,不可逆操作"
                confirmButtonText="确认"
                cancelButtonText="取消"
                confirmButtonType="primary"
                @confirm="handleMultiDelete">
                <template #reference>
                    <el-button type="danger" size="small" v-permission="['batchDeleteWeight,POST']" plain><el-icon><Delete /></el-icon> 批量删除</el-button>
                </template>
            </el-popconfirm>

            <el-button type="danger" size="small"  @click="conditionDelete" v-permission="['ConditionBatchDeleteWeigh,POST']" plain><el-icon><Delete /></el-icon> 条件删除 </el-button>

        </ListHeader>

        <!-- 表格 -->
        <el-table :data="tableData" @selection-change="handleSelectionChange" header-align="center" style="width: 100%; font-size: 1vh;"  v-loading="loading" v-permission="['getListWeight,GET']"  border>
            <el-table-column fixed type="selection" width="40"/>
            <el-table-column prop="type" label="权重类别" align="center" />
            <el-table-column prop="name" label="权重域名" align="center" width="300">
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

            <el-table-column prop="searchweights" label="类型"   align="center">
                <template  #default="{ row }">
                    <span v-for="(item, index) in row.searchweights" :key="index" > 
                        <el-tag class="ml-2"  :color="item.color" effect="light" style="color: #fff !important;">{{ item.en ? item.en : "-"}}</el-tag>
                    </span>
                    
                </template>
            </el-table-column>


            <el-table-column prop="name" label="已汇总数量" align="center" >
                <template  #default="{ row }">
                    <span>{{ row.searchweights ? row.searchweights.length : 0 }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="search_user" label="分配者"  align="center"   />
            <el-table-column prop="first_name" label="创建者"  align="center"   />
            <el-table-column prop="last_name" label="更新者"   align="center"   />
            
            <el-table-column prop="created_at" label="创建时间" align="center"   width="145">
                <template  #default="{ row }">
                    <span>{{ row.created_at ? dateFormat(row.created_at) : '' }}</span>
                </template>
            </el-table-column>

            <el-table-column prop="created_at" label="更新时间"  align="center" width="145">
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
                        v-permission="['modifyWeight,PUT']"
                    /> 

                    <el-popconfirm
                        title="是否要删除该记录"
                        confirmButtonText="确认"
                        cancelButtonText="取消"
                        confirmButtonType="primary"
                        @confirm="handleDelete(scope.row.id)"
                        >
                        <template #reference v-permission="['deleteWeight,DELETE']">
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
        

        <!-- 添加和更新 -->
        <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit">
            <el-form :model="form" ref="formRef" :rules="rules" label-width="80px">
                <el-form-item label="权重域名" prop="name">
                    <el-input v-model="form.name" size="small" placeholder="关键词名称"></el-input>
                </el-form-item>

                <el-form-item label="查询状态" prop="status" >
                    <el-select v-model="form.status" style="width: 100%"   placeholder="" size="small"  clearable filterable>
                        <el-option v-for="(item, index)  in keywordStatus"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                            >
                        </el-option>
                    </el-select>
                </el-form-item>




                <el-form-item label="权重类别" prop="type">
                    <el-select v-model="form.type" style="width: 100%" placeholder="" size="small" clearable filterable >
                        <el-option v-for="(item, index)  in weightTypes"
                            :key="item"
                            :label="item"
                            :value="item"
                            >
                        </el-option>
                    </el-select>
                </el-form-item>



            </el-form>

            
        </FormDrawer>


            <!-- 批量添加 -->
            <el-drawer :title="batchAddTitle" ref="formAddDrawerRef" v-model="batchAddDrawer" size="50%">
                

                <div class="formDrawer">
                    <div class="body">
                        <el-form :model="batchAddForm" ref="formBatchAddRef" :rules="batchAddRules" label-width="80px">
                            <el-form-item label="添加内容" prop="batchContent">
                                <el-input v-model="batchAddForm.batchContent" type="textarea" :rows="20" placeholder="添加的内容，一行一个"></el-input>
                            </el-form-item>


                            <el-form-item label="权重类别" prop="batchType">
                                <el-select v-model="batchAddForm.batchType" style="width: 100%" placeholder="" size="small" clearable filterable >
                                    <el-option v-for="(item, index)  in weightTypes"
                                        :key="item"
                                        :label="item"
                                        :value="item"
                                        >
                                    </el-option>
                                </el-select>
                            </el-form-item>

<!-- 
                            <el-form-item label="过滤规则" prop="batchRule">
                                <el-input v-model="batchAddForm.batchRule" type="textarea" :rows="10" placeholder="请输入需要过滤的顶级域名，只对权重类别选择 二次筛查 有效，一行一个"></el-input>
                            </el-form-item> -->


                        </el-form>
                    </div>
                    <div class="actions">
                        <el-button type="primary" :loading="loading" @click="batchAddsubmit">确定</el-button>
                        <el-button type="default"  @click="batchAddclose">取消</el-button>
                    </div>
                </div>
            </el-drawer>




        
            <!-- 批量添加提示 -->
        <el-dialog :title='existKeyWordTitle'  ref="formDialogRef" v-model="existKeyWordDrawer">
            <span>批量添加成功: <span style="color:green">{{ successTotal }}</span>; </span><span>批量添加失败: <span style="color: red;">{{ errorTotal  }}</span></span>
            
            <el-divider />

            <div>
                <p v-for="item in errorData" :key="item">{{ item }}</p>
            </div>
        </el-dialog>


        <!-- 点击下载完成后提示框 -->
        <el-dialog :title='downloadTitle'  ref="formDialogRef" v-model="downloadDialog">
            
            <el-divider />
            <h3>
                <a :href="'api/' + downloadPath" style="color: green;"  >点击下载</a>
            </h3>
            <el-divider />
        </el-dialog>


        <!-- 条件删除 || 条件更新 完成后提示框 -->
        <el-dialog :title='publicDescTitle'    v-model="publicDialog">
            
            <el-divider />
            <h3>
                <p>{{ publicDesc }}</p>
            </h3>
            <el-divider />
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


        <!-- 条件下载模态框 -->
        <FormDialog :title='DialogTitle'  ref="formTjDialogRef" @submit="dialogSubmit">
            <el-descriptions
                :column="1"
                size="small"
                border
            >
                <el-descriptions-item label="关键词">{{ searchForm.keyword }}</el-descriptions-item>
                <el-descriptions-item label="查询状态">
                    <span v-if="searchForm.status == -2">未查询</span>
                    <span v-else-if="searchForm.status == -1">正在查询</span>
                    <span v-else-if="searchForm.status == 1">已查询</span>
                    <span v-else></span>

                </el-descriptions-item>
                <el-descriptions-item label="权重类型">{{ searchForm.type }}</el-descriptions-item>
                <el-descriptions-item label="域名类型">{{ searchForm.en }}</el-descriptions-item>
                <el-descriptions-item label="创建时间">{{ searchForm.start_end ? searchForm.start_end.join('~') : '' }}</el-descriptions-item>
                <el-descriptions-item label="更新时间">{{ searchForm.update_start_end ? searchForm.update_start_end.join('~'): '' }}</el-descriptions-item>

                <el-descriptions-item label="默认">
                    <el-tag size="small" type="danger">如果以上无数据, 没有条件, 则{{ DialogTitle }}所有,否则{{ DialogTitle }}符合相关数据</el-tag>
                </el-descriptions-item>
            </el-descriptions>

        </FormDialog>


        <!-- 条件删除模态框 -->
        <FormDialog :title='deleteDialogTitle'  ref="formDeleteDialogRef" @submit="deletedialogSubmit">
            <el-descriptions
                :column="1"
                size="small"
                border
            >
                <el-descriptions-item label="关键词">{{ searchForm.keyword }}</el-descriptions-item>
                <el-descriptions-item label="查询状态">
                    <span v-if="searchForm.status == -2">未查询</span>
                    <span v-else-if="searchForm.status == -1">正在查询</span>
                    <span v-else-if="searchForm.status == 1">已查询</span>
                    <span v-else></span>

                </el-descriptions-item>
                <el-descriptions-item label="权重类型">{{ searchForm.type }}</el-descriptions-item>
                <el-descriptions-item label="域名类型">{{ searchForm.en }}</el-descriptions-item>
                <el-descriptions-item label="创建时间">{{ searchForm.start_end ? searchForm.start_end.join('~') : '' }}</el-descriptions-item>
                <el-descriptions-item label="更新时间">{{ searchForm.update_start_end ? searchForm.update_start_end.join('~'): '' }}</el-descriptions-item>

                <el-descriptions-item label="默认">
                    <el-tag size="small" type="danger">如果以上无数据, 没有条件, 则{{ deleteDialogTitle }}所有,否则{{ deleteDialogTitle }}符合相关数据</el-tag>
                </el-descriptions-item>
            </el-descriptions>

        </FormDialog>


        <!-- 条件更新模态框 -->
        <FormDialog :title='ConditionUpdateDialogTitle'  ref="ConditionUpdateDialogRef" @submit="updateConditionDialogSubmit">
            <el-descriptions
                :column="1"
                size="small"
                border
            >
                <el-descriptions-item label="关键词">{{ searchForm.keyword }}</el-descriptions-item>
                <el-descriptions-item label="查询状态">
                    <span v-if="searchForm.status == -2">未查询</span>
                    <span v-else-if="searchForm.status == -1">正在查询</span>
                    <span v-else-if="searchForm.status == 1">已查询</span>
                    <span v-else></span>

                </el-descriptions-item>
                <el-descriptions-item label="权重类型">{{ searchForm.type }}</el-descriptions-item>
                <el-descriptions-item label="域名类型">{{ searchForm.en }}</el-descriptions-item>
                <el-descriptions-item label="创建时间">{{ searchForm.start_end ? searchForm.start_end.join('~') : '' }}</el-descriptions-item>
                <el-descriptions-item label="更新时间">{{ searchForm.update_start_end ? searchForm.update_start_end.join('~'): '' }}</el-descriptions-item>

                <el-descriptions-item label="默认">
                    <el-tag size="small" type="danger">如果以上无数据, 没有条件, 则{{ ConditionUpdateDialogTitle }}所有,否则{{ ConditionUpdateDialogTitle }}符合相关数据</el-tag>
                </el-descriptions-item>
            </el-descriptions>

        </FormDialog>


    
    </el-card>


    

    
</template>


<script setup>
import { ref,reactive,onDeactivated,watchEffect } from 'vue'
import { Delete, Edit } from '@element-plus/icons-vue'
import Search from '@/components/Search.vue'
import SearchItem from '@/components/SearchItem.vue'
import { toast, getNextDate } from '@/utils/tools.js'

import { 
    getWeightList,
    createWeight,
    updateWeight,
    deleteWeight,
    batchCreateWeight,
    batchDeleteWeight,
    batchUpdataWeight,
    getTaskCreateWeight,
    ConditionBatchDeleteWeigh,
    ConditionBatchUpdateWeigh
} from "@/api/weight.js"
import ListHeader from '@/components/ListHeader.vue';
import FormDialog from '@/components/FormDialog.vue'
import FormDrawer from '@/components/FormDrawer.vue';
import { useInitTable,useInitForm } from '@/composables/useCommon'
import { dateFormat,getCurrentTime } from '@/utils/tools.js'
import useClipboard from "vue-clipboard3"
import { exportExcel } from '@/utils/exportExcel'

const keywordStatus = ref([])
const weightTypes = ref([])
const ens = ref([])

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
    multiSelectionIds,
    // handleStatusChange
} = useInitTable({
    searchForm: {
        keyword: '',
        status: '',
        type: '',
        en: '',
        skip: 1,
        limit: 10,
        start_end: '',
        update_start_end: '',
        paging: 1,
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
                weightTypes.value   = res.weightTypes
                ens.value           = res.ens

        },
    getList: getWeightList,
    delete: deleteWeight,
    multidelete: batchDeleteWeight,
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
                message: '状态不能为空',
                trigger: 'blur',
            },],
        type: [{
                required: true,
                message: '类型不能为空',
                trigger: 'blur',
            },],
    },


    getData,
    update: updateWeight,
    create: createWeight
})


const handleSizeChange = (val) => {
  getData()
}
const handleCurrentChange = (val) => {
  getData()
}



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
    batchType: '',
    // batchRule: '',
})
const batchAddRules = {
    batchContent: [
            {
                required: true,
                message: '批量添加内容不能为空',
                trigger: 'blur',
            },
        ],
        batchType: [
            {
                required: true,
                message: '批量添加类型不能为空',
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
        if(!valid) return 

        loading.value = true

    
        batchCreateWeight(batchAddForm).then(res=>{
            task_id.value = res.task_id
            toast(batchAddTitle.value + '成功')
            formBatchAddRef.value.resetFields()
            batchAddDrawer.value = false
            getData()

            // // 如果存在数据，则打开对话框
            // if(res.errorTotal > 0) {
            //     existKeyWordDrawer.value = true
            //     existKeyWordTitle.value = '已存在的数据'
            //     successTotal.value = res.successTotal
            //     errorTotal.value = res.errorTotal
            //     errorData.value = res.errorData
            // }

            percentageLabel.value = '文件上传任务进度 '
            toast('批量添加任务已添加,5秒后开始执行')
            timerLoading.value = setInterval(() => {
                doInterval()   
            }, 3000);

            
            
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
        toast('<p>权重域名: '+ row.name + '</p><p style="margin-top: 10px;color: green;">复制成功</p>');

    } catch (e) {
        toast('复制失败 || 权重域名不存在','warning')
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





// 下载当页数据
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

        if(e.searchweights.length > 0) {
            e.en = e.searchweights[0].en
        } else {
            e.en = ''
        }
        
    });

    return newDate
}

// 下载当页数据
const exportToExcel = ()=> {
    
    loading.value = true

    let newDate = fieldReplace(tableData.value)
    
    let fields = {
        type: "权重类型",
        name: "权重域名",
        status: "查询状态",
        en: "域名类型"
    };


    // let data = JSON.parse(JSON.stringify(this.tableData3));  // 如果直接放置数据不行请加上这句

    exportExcel(newDate, fields, getCurrentTime() + "_权重域名管理");
    getData()

    loading.value = false
}



// 条件下载 或者 条件删除
const formTjDialogRef = ref(null)
const DialogTitle = ref(null)
const conditionToExcel = () => {
    DialogTitle.value = '下载条件'
    formTjDialogRef.value.open()
}

const dialogSubmit = () => {
    // 条件标识及加载
    formTjDialogRef.value.showLoading()
    searchForm.paging = 0
    loading.value = true

    // 从后端获取数据
    getWeightList(searchForm).then(async res => {
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

// 条件删除
const formDeleteDialogRef = ref(false)
const deleteDialogTitle = ref(null)

const conditionDelete = () => {
    deleteDialogTitle.value = '删除条件(仅对二次筛选库有效)'
    formDeleteDialogRef.value.open()
}


const deletedialogSubmit = () => {
    loading.value = true
    formDeleteDialogRef.value.showLoading()
    ConditionBatchDeleteWeigh(searchForm).then(async res=> {
        task_id.value = res.task_id
        percentageLabel.value = '条件删除任务进度 '
        toast('条件删除任务已添加，正在执行，请不要关闭页面，注意观察进度条情况，请耐心等等')
        timerLoading.value = setInterval(() => {
            doIntervalPulic('删除条件数据完成', '总删除：', '删除条件数据完成信息提示', publicDialog)   
        }, 3000);

        formDeleteDialogRef.value.close()
    }).finally(() => {
        loading.value = false
        formDeleteDialogRef.value.hideLoading()
        // resetSearchFrom()
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
        ConditionBatchUpdateWeigh(searchForm, ConditionUpdateChildForm).then(async res=> {
            task_id.value = res.task_id
            percentageLabel.value = '条件更新任务进度 '
            toast('条件更新任务进度已添加，正在执行，请不要关闭页面，注意观察进度条情况，请耐心等等')
            timerLoading.value = setInterval(() => {
                doIntervalPulic('条件更新完成', '总更新：', '更新条件数据完成信息提示', publicDialog)
            }, 3000);

            ConditionUpdataChildDialogRef.value.close()
            ConditionUpdateDialogRef.value.close()
        }).finally(() => {
            loading.value = false
            ConditionUpdateDialogRef.value.hideLoading()
            ConditionUpdataChildDialogRef.value.hideLoading()
        })
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
        batchUpdataWeight(UpdatabatchForm)
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


// 循环获取上传数据定时器
function doInterval() {
    // percentageValue.value = null
    getTaskCreateWeight({'task_id': task_id.value}).then(res => {
            let num = parseInt(res.task.progress)

            

            if (num === 100) {
                percentageValue.value = null
                task_id.value = ''
                clearInterval(timerLoading.value)
                getData()

                // 并展示出来
                var description =  eval('(' + res.task.description + ')');

                toast(`批量导入:${description.insert_total} 条, 更新：${description.update_total} ,失败: ${description.error_total}`, 'warning' )
                existKeyWordTitle.value = '导入错误详情'
                existKeyWordDrawer.value = true
                successTotal.value = description.insert_total
                updateTotal.value = description.update_total
                errorTotal.value = description.error_total
                errorData.value = description.error

            } 
            percentageValue.value = num
        })
}



// 循环获取下载数据定时器
const downloadTitle = ref(null)
const downloadDialog = ref(false)
const downloadPath = ref(null)
function doIntervalDonwLoad() {
    // percentageValue.value = null
    getTaskCreateWeight({'task_id': task_id.value}).then(res => {
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


// 删除条件展示
const publicDesc = ref(null)
const publicDescTitle = ref(null)
const publicDialog = ref(false)
function doIntervalPulic(toastTitle, totalTitle, descTitle, dialog) {
    getTaskCreateWeight({'task_id': task_id.value}).then(res => {
            let num = parseInt(res.task.progress)

            if (num >= 100) {
                percentageValue.value = null
                task_id.value = ''
                clearInterval(timerLoading.value)
                // 并展示出来
                toast(toastTitle)
                publicDesc.value = totalTitle + res.task.description
                publicDescTitle.value = descTitle
                

                setTimeout(()=> {
                    dialog.value = true
                },1000)
                getData()

            } 
            percentageValue.value = num
        })
}



onDeactivated(() => {
    clearInterval(timerLoading.value);
    percentageValue.value = null
})


</script>


