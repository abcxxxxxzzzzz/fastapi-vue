<template>
    <el-card shadow="always" class="border-0">
        
        <!-- 搜索 -->
        <Search @model="searchForm" @search="getData" @reset="resetSearchFrom">
            <SearchItem label="搜索">
                <el-input v-model="searchForm.keyword" placeholder="模糊搜索电话号码" clearable @keyup.enter="getData" v-on:input="getData"></el-input>
            </SearchItem>

                        <!-- 添加到自定义插槽 -->
            <template #show>

                <SearchItem label="创建人">
                        <el-select v-model="searchForm.first_name"  placeholder="" clearable filterable style="width: 40vh;">
                            <el-option v-for="(item, index)  in f_users"
                                :key="item.first_name"
                                :label="item.first_name"
                                :value="item.first_name"
                                >
                            </el-option>
                        </el-select>
                    </SearchItem>



                    
                <SearchItem label="更新人">
                    <el-select v-model="searchForm.last_name"  placeholder="" clearable filterable>
                        <el-option v-for="(item, index)  in l_users"
                            :key="item.last_name"
                            :label="item.last_name"
                            :value="item.last_name"
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
                    v-show="percentageValue > 0"
                    >
                
                    <template #default="{ percentage  }">
                        <span class="percentage-label">{{ percentageLabel }}</span>
                        <span class="percentage-value">{{ percentageValue }}%</span>
                        
                    </template>
                </el-progress>


        <!-- <ListHeader @create="handleCreate" @refresh="getData" v-permission="['createIphoneNumber,POST']"></ListHeader> -->
        <ListHeader layout="refresh,download,condition"  @download="exportToExcel" @condition="conditionToExcel" @refresh="getData">
            <el-button type="primary" size="small" @click="handleCreate" v-permission="['createIphoneNumber,POST']"><el-icon><Plus /></el-icon> 新增</el-button>
            <el-popconfirm
                title="是否要批量彻底删除选择的记录,不可逆操作"
                confirmButtonText="确认"
                cancelButtonText="取消"
                confirmButtonType="primary"
                @confirm="handleMultiDelete">
                <template #reference>
                    <el-button type="danger" size="small" v-permission="['batchDeleteIphoneNumber,POST']"><el-icon><Delete /></el-icon> 批量删除</el-button>
                </template>
            </el-popconfirm>

            <el-button  plain size="small"  @click="openUploadFile"  v-permission="['batchImportIphoneNumber,POST']"><el-icon><Upload /></el-icon> 文件上传</el-button>

        
        
        </ListHeader>

        <!-- 表格 -->
        <vxe-table
            border
            max-height="800"
            show-overflow
            ref="multipleTableRef"
            :data="tableData"
            class="mytable-scrollbar"
            header-align="center" 
            style="width: 100%; font-size: 1vh; height: 100%;"  
            :loading="loading" 
            @checkbox-all="handleSelectionChangeEvent"
            @checkbox-change="handleSelectionChangeEvent" 
            :row-config="{isCurrent: true, isHover: true}"
            :sort-config="{chronological: true, remote: true}"
            @sort-change="SortVxeChangeEvent"
            v-permission="['getListIphoneNumber,GET']"
            >

            <vxe-column type="checkbox" align="center"  width="5%"></vxe-column>
            <vxe-column field="number"      title="手机号码"   align="center" ></vxe-column>
            <vxe-column field="first_name"  title="创建人"   align="center" ></vxe-column>
            <vxe-column field="last_name"   title="更新人"   align="center" ></vxe-column>

            <vxe-column field="created_at"  title="创建时间" align="center" sortable>
                <template  #default="{ row }">
                    <span>{{ row.created_at ? dateFormat(row.created_at) : '' }}</span>
                </template>
            </vxe-column>

            <vxe-column  field="updated_at" title="更新时间" align="center" sortable>
                <template  #default="{ row }">
                    <span>{{ row.updated_at ? dateFormat(row.updated_at) : ''  }}</span>
                </template>
            </vxe-column>

        
            <vxe-column  title="操作" fixed="right" >
                <template #default="{ row }">
                    <el-button 
                        size="small" 
                        :icon="Edit"
                        @click="handleEdit(row)"
                        v-permission="['updateIphoneNumber,PUT']"
                    /> 

                    <el-popconfirm
                        title="是否要删除该记录"
                        confirmButtonText="确认"
                        cancelButtonText="取消"
                        confirmButtonType="primary"
                        @confirm="handleDelete(row.id)"
                        >
                        <template #reference>
                            <el-button size="small" :icon="Delete" type="danger" v-permission="['deleteIphoneNumber,DELETE']"/>
                        </template>
                    </el-popconfirm>
                </template>
            </vxe-column>

            
        </vxe-table>

          <!-- 分页 -->
          <vxe-pager
            :layouts="['Sizes', 'PrevJump', 'PrevPage', 'Number', 'NextPage', 'NextJump', 'FullJump', 'Total']"
            :pageSizes="[10, 50, 200, 500, 1000, 5000, 10000, 20000, 50000]"
            v-model:current-page="searchForm.skip"
            v-model:page-size="searchForm.limit"
            :total="total"
            @page-change="handleCurrentChange">

            <template #right>
                <div class="flex justify-between justify-center">
                    <img src="@/assets/img/89fc-fyscsmv5911424.gif" height="10" width="30">
                    <img src="@/assets/img/89fc-fyscsmv5911424.gif" height="10" width="30">
                    <img src="@/assets/img/89fc-fyscsmv5911424.gif" height="10" width="30">
                </div>
                
          </template>
        </vxe-pager>



        <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit">
            <el-form :model="form" ref="formRef" :rules="rules" label-width="80px">
                <el-form-item label="手机号码" prop="number">
                    <el-input v-model="form.number"  placeholder="手机号码"></el-input>
                </el-form-item>
            </el-form>
        </FormDrawer>




        <!-- 上传 -->
        <el-drawer title="文件上传" v-model="drawer" >
            <el-upload
                class="upload-demo"
                drag
                action
                ref="upload"
                accept=".xlsx,.xls"
                :limit="1"
                :show-file-list="true"
                :auto-upload="false"
                :before-upload="beforeUpload"
                :on-change="UploadOnChange"
                :on-remove="UploadRemove"
                :on-exceed="UploadExceed"
            >
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                <div class="el-upload__text" >
                    拖入文件到这里 或者<em> 点击上传</em>
                </div>
                <template #tip>
                    <div class="el-upload__tip">
                        <el-divider />
                        xlsx/xls 结尾格式; <button text @click="exportToExcelTemplate" style="color: green">模板下载</button>
                        <el-divider />
                        <!-- <h3 style="color: red">注意: 已存在数据会更新,不存在数据添加</h3>  -->
                        <p>手机号码: <span style="color: red">*必须*</span></p>
                        <el-divider />
                    </div>
                    <!-- <div class="el-upload__tip"> -->
                        <h3 style="color: green;">EXCEL转化后 JSON 总数据: <span style="color: red">{{ excelDataLength }}</span> 条</h3> 
                    <!-- </div> -->
                    
                </template>

                
                
            </el-upload>

            
            <el-button size="small" type="primary" @click="handleImport" style="width: 100%">导入</el-button>

        </el-drawer>



        <!-- 批量导入错误提示框 -->
        <el-dialog :title='importTitle'  width="50%" v-model="importModel">
            <span>导入新数据: 
                <span style="color:green; margin: 0 1vh;">{{ successTotal }} </span>条; 
            </span>

            <!-- <span>导入更新数据: 
                <span style="color: chocolate; margin: 0 1vh;" >{{ updateTotal  }} </span>条;
            </span> -->

            <span>导入失败重复数据: 
                <span style="color: red; font-size: 20px; background-color: black; border-radius: 50%; margin: 0 1vh;">{{ errorTotal  }} </span>条
            </span>
            
            
            <el-divider />
                    <vxe-table
                        align="center"
                        :data="errorData">
                        <vxe-column field="number" title="手机号码"></vxe-column>
                    </vxe-table>

        </el-dialog>



        
        <!-- 条件下载模态框 -->
        <FormDialog :title='DialogTitle'  ref="formDialogRef" @submit="dialogSubmit">
            <el-descriptions
                title="下载到 EXCEL 条件内容"
                :column="1"
                size="small"
                border
            >
                <el-descriptions-item label="搜索号码">{{ searchForm.keyword }}</el-descriptions-item>
                <el-descriptions-item label="创建人">{{ searchForm.contact_user }}</el-descriptions-item>
                <el-descriptions-item label="更新人">{{ searchForm.last_name }}</el-descriptions-item>
                <el-descriptions-item label="创建时间">{{ searchForm.start_end ? searchForm.start_end.join('~') : '' }}</el-descriptions-item>
                <el-descriptions-item label="更新时间">{{ searchForm.update_start_end ? searchForm.update_start_end.join('~'): '' }}</el-descriptions-item>

                <el-descriptions-item label="默认">
                    <el-tag size="small" type="danger">如果以上无条件, 则下载所有,否则下载符合相关条件数据</el-tag>
                </el-descriptions-item>
            </el-descriptions>
        </FormDialog>




    </el-card>


    

    
</template>


<script setup>
import { 
    getListIphoneNumber,
    createIphoneNumber,
    updateIphoneNumber,
    deleteIphoneNumber,
    multiFromExcelImportIphoneNumber,
    batchDeleteIphoneNumber,
    getTaskIphoneNumber,
} from "@/api/iphoneNumber.js"

import { ref,reactive,computed,watchEffect,onMounted,onDeactivated   } from 'vue'
import { Delete, Edit } from '@element-plus/icons-vue'
import { useInitTable,useInitForm } from '@/composables/useCommon'
import { dateFormat,getNextDate,getCurrentTime,toast } from '@/utils/tools.js'
import Search from '@/components/Search.vue'
import SearchItem from '@/components/SearchItem.vue'
import FormDialog from '@/components/FormDialog.vue'
import ListHeader from '@/components/ListHeader.vue';
import FormDrawer from '@/components/FormDrawer.vue';
import { exportExcel,ImporExceltToJson } from '@/utils/exportExcel'



const f_users = ref([])
const l_users = ref([])

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
    multipleTableRef,
    handleMultiDelete,
    multiSelectionIds,
} = useInitTable({
    searchForm: {
        keyword: '',
        skip: 1,
        limit: 10,
        field:'',
        order_by: '',
        first_name: '',
        last_name: '',
        start_end: '',
        update_start_end: '',
        paging: 1,
    },
    rules: {
        number: [{
                    required: true,
                    message: '标签名称不能为空',
                    trigger: 'blur',
                },],
    },
    onGetListSuccess: (res)=> {
        tableData.value = res.list.map(o=>{
            o.statusLoading = false
            return o
        })

        total.value = res.totalCount
        f_users.value = res.f_users
        l_users.value = res.l_users
    },

    getList: getListIphoneNumber,
    delete: deleteIphoneNumber,
    multidelete: batchDeleteIphoneNumber,
    // updateStatus: updateGroupStatus
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
        number:'',
    },
    rules: {
        number: [{
                required: true,
                message: '手机号码不能为空',
                trigger: 'blur',
            },],
    },

    getData,
    update: updateIphoneNumber,
    create: createIphoneNumber
})


// 分页触发
const handleCurrentChange = (val) => {
  getData()
}


// 触发获取 CheckBox 选中
const handleSelectionChangeEvent = (val) => {
    const $table = multipleTableRef.value
    const selectRecords = $table.getCheckboxRecords()
    let _ids = []
    selectRecords.forEach(e => {
        _ids.push(e.id)
    });
    multiSelectionIds.value = _ids
}


// 触发排序
const SortVxeChangeEvent  = (val) => {
    searchForm['field'] = val.field
    searchForm['order_by'] = val.order
    getData()
}



// 返回下载数据头
function excelField() {
    let _fds = {
        number: "手机号码",
        first_name: "创建人",
        last_name: "更新人",
        created_at: "创建时间",
        updated_at: "更新时间",
    };
    return _fds
}



// // 导出替换某些字段
// function fieldReplace(newDate) {
    
//     newDate.forEach(e => {

//         // 如果彩金与会员库存在关联, 并且彩金管理ID与会员库ID相等
//         if (e.members && e.member_id == e.members.id) {
//             e.username =  e.members.username

//             // 如果会员有归属部门,则获取部门名字
//             if(e.members.owner) {
//                 if(e.members.owner_id == e.members.owner.id) {
//                     e.owner = e.members.owner.name
//                 }
//             } else {
//                 e.owner =  '未知'
//             }

//         } else {
//             e.username =  '未知'
//         }



//         // 如果彩金与彩金来源存在关联
//         if (e.sources && e.source_id == e.sources.id) {
//             e.source =  e.sources.name
//         } else {
//             e.source =  '未知'
//         }


//     });

//     return newDate
// }



// 当页下载
const exportToExcel = (val)=> {

    loading.value = true

    // let newDate = fieldReplace(tableData.value)
    let newDate = tableData.value
    
    let fields = excelField()

    exportExcel(newDate, fields, getCurrentTime());
    // getData()

    loading.value = false
}








// 条件下载
// const keywordName = ref(null)
const formDialogRef = ref(null)
const DialogTitle = ref(null)
const conditionToExcel = () => {
    // let _asyncwd = []
    // searchForm.asynckeyword.forEach(e => {
    //     existSearchs.value.map(o => {
    //         // console.log(o.id, e)
    //         if(o.id == e) {
    //             o.name = o.username
    //             _asyncwd.push(o.name)
    //         }
            
    //     })
    // });
    
    // keywordName.value = _asyncwd

    DialogTitle.value = '条件下载确认'
    formDialogRef.value.open()
}



const dialogSubmit = () => {
    formDialogRef.value.showLoading()

    // 条件下载标识
    searchForm.paging = 0
    // 获取
    loading.value = true
    // 从后端获取数据
    getListIphoneNumber(searchForm).then(async res => {
        toast('数据已获取，开始转换下载......，数据量大的话，会出现卡顿状态，请耐心等等')
        setTimeout(async ()=> {
            let newDate = res.list
            let fields = excelField()
            await exportExcel(newDate, fields, getCurrentTime() + "_彩金管理");
        }, 1000)
    
        formDialogRef.value.close()
        // getData()
    }) .finally(()=>{
        loading.value = false
        searchForm.paging = 1
        formDialogRef.value.hideLoading()
    })
} 





// 导入
const drawer = ref(false)
const upload = ref(null)
const importTitle = ref(null)
const importModel = ref(false)
const ImportFromExcelJson = ref([])
const excelDataLength = ref(0)
const successTotal = ref(0)
// const updateTotal = ref(0)
const errorTotal = ref(0)
const errorData = ref([])


const openUploadFile = ()=> drawer.value = true

const beforeUpload = (e) => {
    const TYPE = ['xls', 'xlsx']
    const extension = TYPE.includes(e.name.split('.')[1])

    const isLt2M = e.size / 1024 / 1024 < 5

    if (!extension) {
        toast('上传模板只能是 xls、xlsx格式!', 'warning')
        return false
    }

    if (!isLt2M) {
        toast('上传模板大小不能超过 5MB!', 'warning')
        return false
    }
    return true
}



// 导入模板下载
const exportToExcelTemplate = ()=> {
    let fields = excelField()
    delete fields.first_name
    delete fields.last_name
    delete fields.created_at
    delete fields.updated_at
    exportExcel([], fields, '手机号码模板');

}

// 点击上传触发
const  UploadOnChange =  async (ev) => {

    toast('检查数据....', 'warning')
    try {
        setTimeout(async () => {
            loading.value = true
            let data = await ImporExceltToJson(ev)
            let arr = []                    // 存放替换后端接受的格式
            
            data.forEach((item) => {
                if (typeof(item["手机号码"]) === 'undefined') {
                    loading.value = false
                    upload.value.clearFiles()
                    toast('手机号码表头不能为空', 'error')
                    throw new Error('手机号码表头不能为空')
                }

                let _replace = {                     // 替换对象
                    number: item["手机号码"],
                }
                arr.push(_replace);
            });

            ImportFromExcelJson.value = arr
            
            
            
            excelDataLength.value = ImportFromExcelJson.value.length
            loading.value = false
            toast('检查表格格式完毕....')
            // console.log('总共导入多少条数据:', ImportFromExcelJson.value.length)
        }, 100)
    } catch (e) {
        toast('异常错误：'+e, 'error')
    } finally {
        loading.value = false
    }


}


// 移除上传文件触发
const UploadRemove = async (ev) => {
    toast(`移除文件: ${ ev.name}`, 'info')
    ImportFromExcelJson.value = []
    excelDataLength.value = 0
}

// 上传文件超出限制触发
const UploadExceed = async (ev) => {
    toast('超出上传文件最大限制,请先移除已有 EXCEL 文件', 'warning')
}

// 触发 EXCEL 导入
const handleImport = () =>{

    if (ImportFromExcelJson.value.length === 0 ) return toast('无数据添加', 'info')

    // 组合 END
    loading.value = true
    multiFromExcelImportIphoneNumber({'importData': ImportFromExcelJson.value})
    .then(res=> {
        drawer.value = false
        upload.value.clearFiles() // 清空上传列表
        getData()

        toast('导入任务已在后台运行')
        timer.value = setInterval(() => {
            doInterval()   
        }, 1000);
        // toast(res.msg)
        // console.log(res)
        // if(res.error_data.length > 0) {
        //     toast(`批量导入:${res.insert_total} 条, 失败: ${res.error_data.length}`, 'warning' )
        //     importTitle.value = '导入错误详情'
        //     importModel.value = true
        //     console.log(res.error_data)
        //     successTotal.value = res.insert_total
        //     errorTotal.value = res.error_data.length
        //     errorData.value = res.error_data
        // } else {
        //     toast(`批量导入:${res.insert_total} 条, 失败: ${res.error_data.length}`, )
        // }
        

    })
    .finally(()=>{
        loading.value = false
    })
}


// 时间格式
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




// 进度条
const timer = ref(null)
const colors = [
  { color: '#f56c6c', percentage: 20 },
  { color: '#e6a23c', percentage: 40 },
  { color: '#5cb87a', percentage: 60 },
  { color: '#1989fa', percentage: 80 },
  { color: '#6f7ad3', percentage: 100 },
]

const percentageLabel = ref(null)
const percentageValue = ref(0)
watchEffect(() => {
    percentageLabel.value = '文件上传任务进度 '
    if(percentageValue.value == 100) {
        setTimeout(()=>{
            clearInterval(timer.value)
        },1000)
    }

    
})


// 循环定时器
function doInterval() {
    getTaskIphoneNumber().then(res => {
            let num = parseInt(res.progress)
            if (num === 100) {
                percentageValue.value = 0
                clearInterval(timer.value)
                return false
            } 
            percentageValue.value = num
        })
}


// timer.value = setInterval(() => {
//     doInterval()   
// }, 1000);



onDeactivated(() => {
    clearInterval(timer.value);
})




onMounted(() => {
    timer.value = setInterval(() => {
        doInterval()   
    }, 1000);
})



</script>