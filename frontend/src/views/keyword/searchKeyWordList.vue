<template>
    <el-card shadow="always" class="border-0">
        
        <Search @model="searchForm" @search="getData" @reset="resetSearchFrom">

            <SearchItem label="词汇来源">
                <el-select v-model="searchForm.type"  placeholder="" clearable filterable>
                    <el-option v-for="(item, index)  in types"
                        :key="item"
                        :label="item"
                        :value="item"
                        >
                    </el-option>
                </el-select>
            </SearchItem>


            <SearchItem label="关键词">
                <el-select
                    v-model="searchForm.asynckeyword"
                    multiple
                    filterable
                    remote
                    reserve-keyword
                    placeholder="已搜索关键词,可多选"
                    :remote-method="remoteMethod"
                    :loading="selectRemoteLoading"
                    size="small"
                    clearable
                    @change="getData"
                    style="width: 30vh;"
                >
                    <el-option
                        v-for="item in options"
                        :key="item.id"
                        :label="item.name"
                        :value="item.id"
                    />
                </el-select>
            </SearchItem>


            <SearchItem label="其他内容">
                    <el-input
                        placeholder="模糊搜索对应链接、网站网址、联系方式、备注"
                        v-model="searchForm.keyword"
                        @keyup.enter="getData"
                        v-on:input="getData"
                        >
                    </el-input>
            </SearchItem>
            

            <!-- 添加到自定义插槽 -->
            <template #show>

                

                <SearchItem label="排名序号">
                    <el-select v-model="searchForm.number"   placeholder="" clearable filterable>
                        <el-option v-for="(item, index) in numbers"
                            :key="item.number"
                            :label="item.number"
                            :value="item.number">
                        </el-option>
                    </el-select>
                </SearchItem>


                <SearchItem label="类型">
                    <el-select v-model="searchForm.en"  placeholder="" clearable filterable>
                        <el-option v-for="(item, index)  in ens"
                            :key="item.en"
                            :label="item.en"
                            :value="item.en"
                            >
                        </el-option>
                    </el-select>
                </SearchItem>

                <SearchItem label="是否锁定">
                    <el-select v-model="searchForm.lock"   placeholder="" clearable filterable style="width: 30vh;">
                        <el-option v-for="(item, index) in is_locks"
                            :key="item.is_contact"
                            :label="item.label"
                            :value="item.is_contact">
                        </el-option>
                    </el-select>
                </SearchItem>

                <SearchItem label="导入者">
                    <el-select v-model="searchForm.first_name"  placeholder="" clearable filterable style="width: 40vh;">
                        <el-option v-for="(item, index)  in first_names"
                            :key="item.username"
                            :label="item.username"
                            :value="item.username"
                            >
                        </el-option>
                    </el-select>
                </SearchItem>


                <SearchItem label="执行者">
                    <el-select v-model="searchForm.contact_user"  placeholder="" clearable filterable>
                        <el-option v-for="(item, index)  in contact_users"
                            :key="item.username"
                            :label="item.username"
                            :value="item.username"
                            >
                        </el-option>
                    </el-select>
                </SearchItem>



                



                

                <SearchItem label="更新者">
                    <el-select v-model="searchForm.last_name"  placeholder="" clearable filterable>
                        <el-option v-for="(item, index)  in last_names"
                            :key="item.username"
                            :label="item.username"
                            :value="item.username"
                            >
                        </el-option>
                    </el-select>
                </SearchItem>

                <SearchItem label="联系方式">
                    <el-select v-model="searchForm.is_contact"  placeholder="" clearable filterable>
                        <el-option v-for="(item, index)  in is_contacts"
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
                        :shortcuts="shortcuts"
                        range-separator="到"
                        start-placeholder="开始时间"
                        end-placeholder="结束时间"
                        format="YYYY-MM-DD HH:mm:ss"
                        value-format="YYYY-MM-DD HH:mm:ss"
                        :default-time="defaultTime"
                        />
                </SearchItem>

                <SearchItem label="更新时间">

                    <el-date-picker
                        v-model="searchForm.update_start_end"
                        type="datetimerange"
                        :shortcuts="shortcuts"
                        range-separator="到"
                        start-placeholder="开始时间"
                        end-placeholder="结束时间"
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
            :color="progresscolors"
            class="mb-6"
            v-show="percentageValue != null"
            >
        
            <template #default="{ percentage  }">
                <span class="percentage-label">{{ percentageLabel }}</span>
                <span class="percentage-value">{{ percentageValue }}%</span>
                
            </template>
        </el-progress>


        <!-- 表格头部 --> 
        <ListHeader :Interval="true"  layout="refresh,download,condition"  @download="exportToExcel" @condition="conditionToExcel" @refresh="getData">
        
            <el-button type="primary" size="small" @click="handleCreate"  v-permission="['createSearchKeyWord,POST']"><el-icon><Plus /></el-icon> 新增</el-button>
            <el-popconfirm
                title="是否要批量彻底删除选择的记录,不可逆操作"
                confirmButtonText="确认"
                cancelButtonText="取消"
                confirmButtonType="primary"
                @confirm="handleMultiDelete">
                <template #reference>
                    <el-button type="danger" size="small" v-permission="['batchDeleteSearchKeyWord,POST']"><el-icon><Delete /></el-icon> 批量删除</el-button>
                </template>
            </el-popconfirm>

            <el-button type="warning" size="small" v-permission="['handleBatchLock,POST']" @click="handleBatchLock"><el-icon><Lock /></el-icon>批量锁定</el-button>
        
        </ListHeader>

        <!-- 表格 -->
        <vxe-table
            border
            max-height="800"
            show-overflow
            ref="xTableRef"
            :data="tableData"
            class="mytable-scrollbar"
            header-align="center" 
            style="width: 100%; font-size: 1vh; height: 100%;"  
            :loading="loading" 
            v-permission="['getListSearchKeyWord,GET']" 
            @checkbox-all="handleSelectionChangeBefore"
            @checkbox-change="handleSelectionChangeBefore" 
            >

            <vxe-column type="checkbox" align="center"  width="55"></vxe-column>


            <vxe-column prop="type" title="词汇来源" align="center" width="80">
                <template  #default="{ row }">
                    <span>{{ row.owner ? row.owner.type : '未知' }}</span>
                </template>
            </vxe-column>


            <vxe-column prop="owner" title="关键词名称" align="center" width="200">
                <template  #default="{ row }">
                    <span>{{ row.owner ? row.owner.name : '未知' }}</span>
                    <el-button text size="small" circle @click="copy(row)" ><el-icon ><CopyDocument /></el-icon></el-button>
                </template>
            </vxe-column>





            <vxe-column prop="number" field="number" title="排名"    align="center"  width="55"/>
            <vxe-column   title="对应链接"    align="center" width="115">
                    <template  #default="{ row }">
                        <el-tooltip :content="row.link"  placement="top" effect="customized">
                        <!-- <el-tooltip :content="row.link" placement="top" > -->
                            <el-button text size="small" @click.native="goLink(row)" :type="isChange.includes(row.id) ? 'danger' : 'primary'">点击打开</el-button>
                        </el-tooltip>
                    </template>
            </vxe-column>
            <vxe-column  field="url_website" title="网站网址"    align="center" width="200" />
            <vxe-column field="contact" title="联系方式"   align="center" width="150"/>

            <vxe-column title="类型"   align="center" width="100">
                <template  #default="{ row }">
                    <el-tag class="ml-2"  :color="row.color" effect="light" style="color: #fff !important;">{{ row.en ? row.en : "-"}}</el-tag>
                </template>
            </vxe-column>


            <vxe-column  title="已锁定？" align="center" width="100" >
                <template  #default="{ row }">
                    <!-- <span>{{ row.is_contact }}</span> -->
                    <el-switch 
                        v-model="row.is_contact" 
                        class="ml-2"
                        inline-prompt
                        style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
                        active-text="已锁定？"
                        inactive-text="未锁定"
                        :active-value="1" 
                        :inactive-value="0"
                        :statusLoading = "row.statusLoading"
                        :disabled="row.is_contact == 1 && $store.state.user.username != row.contact_user"
                        @change="handlerChangeStatus($event,row)">
                        <!-- :before-change="beforeChangeStatus.bind(this, row)" -->
                    </el-switch>

                </template>
            </vxe-column>

            <vxe-column field="description" title="备注"   align="center" width="130"/>

            <vxe-column field="contact_user" title="执行者"   align="center"  width="60"/>
            

            <vxe-column field="first_name" title="导入者"   align="center" width="60"/>
            <vxe-column field="last_name" title="更新者"    align="center" width="60"/>


            <vxe-column title="创建时间" align="center" width="165" >
                <template  #default="{ row }">
                    <span>{{ row.created_at ? dateFormat(row.created_at) : '' }}</span>
                </template>
            </vxe-column>

            <vxe-column  title="更新时间" align="center" width="165" >
                <template  #default="{ row }">
                    <span>{{ row.updated_at ? dateFormat(row.updated_at) : ''  }}</span>
                </template>
            </vxe-column>


<!-- 
            <vxe-column title="更新时间"  align="center" width="165" >
                <template  #default="{ row }">
                    <span>{{ row.updated_at ? dateFormat(row.updated_at) : ''  }}</span>
                </template>
            </vxe-column> -->



            <vxe-column  title="操作" fixed="right" width="110" >
                <template #default="{ row }">
                    <el-button 
                        :loading = 'editLoading'
                        size="small" 
                        :icon="Edit"
                        @click="handleEditBefore(row)"
                        v-permission="['modifySearchKeyWord,PUT']"
                    /> 

                    <el-popconfirm
                        title="是否要删除该记录"
                        confirmButtonText="确认"
                        cancelButtonText="取消"
                        confirmButtonType="primary"
                        @confirm="handleDelete(row.id)"
                        >
                        <template #reference v-permission="['deleteSearchKeyWord,DELETE']">
                            <el-button size="small" :icon="Delete" type="danger" />
                        </template>
                    </el-popconfirm>
                </template>
            </vxe-column>

            
          </vxe-table>

          <!-- 分页 -->
          <vxe-pager
            :layouts="['Sizes', 'PrevJump', 'PrevPage', 'Number', 'NextPage', 'NextJump', 'FullJump', 'Total']"
            :pageSizes="[10, 50, 200, 500, 1000, 5000, 10000, 20000, 50000, 100000, 200000, 3000000, 5000000, 1000000]"
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


        <!-- 新增|修改 -->
        <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit">
            <el-form :model="form" ref="formRef" :rules="rules" label-width="80px">
                <el-form-item label="关键词" prop="owner_id">

                    <!-- <el-select-v2 
                        v-model="form.owner_id" 
                        style="width: 100%" 
                        placeholder="请选择" 
                        clearable filterable
                        :options="optionsKeyWord"
                    >
                    </el-select-v2> -->
                    <el-select
                        v-model="form.owner_id" 
                        filterable
                        remote
                        reserve-keyword
                        placeholder="输入关键词"
                        :remote-method="remoteMethodTwo"
                        :loading="selectRemoteLoadingTwo"
                        size="small"
                        clearable
                        style="width: 100%"
                    >
                        <el-option
                            v-for="item in optionsTwo"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
                        >
                        </el-option>
                    </el-select>

                </el-form-item>

                <el-form-item label="排名序号" prop="number">
                    <el-input-number v-model="form.number" size="small" ></el-input-number>
                </el-form-item>

                <el-form-item label="对应链接" prop="link">
                    <el-input v-model="form.link"  placeholder="对应链接,请已 http 或者 https 开头"></el-input>
                </el-form-item>

                <el-form-item label="网站网址" prop="url_website">
                    <el-input v-model="form.url_website"  placeholder="网站网址"></el-input>
                </el-form-item>

                <el-form-item label="联系方式" prop="contact">
                    <el-input v-model="form.contact"  placeholder="联系方式"></el-input>
                </el-form-item>

                <el-form-item label="英文" prop="en">
                    <el-select v-model="form.en"  placeholder="" clearable filterable>
                        <el-option v-for="(item, index) in ens"
                            :key="item.en"
                            :label="item.en"
                            :value="item.en"
                            >
                        </el-option>
                    </el-select>
                </el-form-item>

                

                <el-form-item label="颜色" prop="color">
                    <el-select v-model="form.color"  placeholder="" clearable filterable>
                        <el-option v-for="(item, index)  in colors"
                            :key="item.color"
                            :label="item.color"
                            :value="item.color"
                            >
                        </el-option>
                        
                    </el-select>
                    <el-tag class="ml-2"  :color="form.color" effect="light"></el-tag>
                </el-form-item>

                <el-form-item label="备注" prop="description" label-width="80px">
                    <el-input v-model="form.description"  placeholder="备注"></el-input>
                </el-form-item>

            </el-form>
        </FormDrawer>


        

        <!-- 条件下载模态框 -->
        <FormDialog :title='DialogTitle'  ref="formTjDialogRef" @submit="dialogSubmit">
            <el-descriptions
                title="下载到 EXCEL 条件内容"
                :column="1"
                size="small"
                border
            >
                <!-- <el-descriptions-item label="关键词">{{ keywordName ? keywordName.join(',') :'-' }}</el-descriptions-item> -->
                <el-descriptions-item label="其他内容">{{ searchForm.keyword }}</el-descriptions-item>
                <el-descriptions-item label="排名序号">{{ searchForm.number }}</el-descriptions-item>
                <el-descriptions-item label="类型">{{ searchForm.en }}</el-descriptions-item>
                <el-descriptions-item label="是否锁定">
                    <span v-if="searchForm.lock == ''"></span>
                    <span v-else-if="searchForm.lock == 1">已锁定</span>
                    <span v-else>未锁定</span>

                </el-descriptions-item>
                <el-descriptions-item label="导入者">{{ searchForm.first_name }}</el-descriptions-item>
                <el-descriptions-item label="执行者">{{ searchForm.contact_user }}</el-descriptions-item>
                <el-descriptions-item label="更新者">{{ searchForm.last_name }}</el-descriptions-item>
                <el-descriptions-item label="创建时间">{{ searchForm.start_end ? searchForm.start_end.join('~') : '' }}</el-descriptions-item>
                <el-descriptions-item label="更新时间">{{ searchForm.update_start_end ? searchForm.update_start_end.join('~'): '' }}</el-descriptions-item>

                <el-descriptions-item label="默认">
                    <el-tag size="small" type="danger">如果以上无数据, 没有条件, 则下载所有,否则下载符合相关条件数据</el-tag>
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
import { ref,onMounted,watchEffect,onDeactivated } from 'vue'
import {  Delete, Edit } from '@element-plus/icons-vue'
import Search from '@/components/Search.vue'
import SearchItem from '@/components/SearchItem.vue'
import FormDialog from '@/components/FormDialog.vue'

import { 
    getSearchKeyWordList,
    createSearchKeyWord,
    updateSearchKeyWord,
    deleteSearchKeyWord,
    lockSearchKeyWord,
    batchDeleteSearchKeyWord,
    getSearchKeyWordGroupBy,
    batchLockSearchKeyWord,
    searchKeyword,
    showSearchKeyWord,
    getTaskProgress
} from "@/api/searchKeyWord.js"

import {
    getBatchSearchKeyWordCount,
    getSearchKeyWordCount,
    getSearchKeyWordGroupByNumber,
    getSearchKeyWordGroupByUser,
    getSearchKeyWordGroupByEn,
    getSearchKeyWordGroupByCountAt
    
} from "@/api/searchkeywordcount.js"

import ListHeader from '@/components/ListHeader.vue';
import FormDrawer from '@/components/FormDrawer.vue';
import { useInitTable,useInitForm } from '@/composables/useCommon'
import { dateFormat,toast,getNextDate,getCurrentTime } from '@/utils/tools.js'
import useClipboard from "vue-clipboard3"
import { exportExcel } from '@/utils/exportExcel'


const existSearchs = ref([])
const keywords = ref([])
const numbers = ref([])
const is_locks = ref([])
const contact_users = ref([])
const first_names = ref([])
const last_names = ref([])
const ens = ref([])
const colors = ref([])
const types = ref([])
const is_contacts = ref([])


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
    // handleMultiDelete,
    // handleSelectionChange,
    // handleStatusChange
} = useInitTable({
    searchForm: {
        asynckeyword: '',
        keyword: '',
        skip: 1,
        limit: 10,
        number: '',
        lock: '',
        contact_user: '',
        first_name: '',
        last_name: '',
        start_end: '',
        update_start_end: '',
        paging: 1,
        en: '',
        type: '',
        is_contact: '',
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
            // is_locks.value = res.is_locks
            // contact_users.value = res.contact_users
            // first_names.value = res.first_names
            // last_names.value = res.last_names
        },


    getList: getSearchKeyWordList,
    delete: deleteSearchKeyWord,
    // multidelete: batchDeleteSearchKeyWord,
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
        owner_id:'',
        number: 0,
        link: '',
        url_website: '',
        contact: '',
        cn: '',
        en: '',
        color: '',
        description: ''
    },
    rules: {
        owner_id: [{
                required: true,
                message: '排名序号不能为空',
                trigger: 'blur',
            },],
        number: [{
                required: true,
                message: '排名序号不能为空',
                trigger: 'blur',
            },],
        link: [{
            required: true,
            message: '对应链接不能为空',
            trigger: 'blur',
        },],
        url_website: [{
            required: true,
            message: '网站网址不能为空',
            trigger: 'blur',
        },],
        contact: [{
            required: true,
            message: '联系方式不能为空',
            trigger: 'blur',
        },],
            

        // color: [{
        //         required: true,
        //         message: '标签颜色不能为空',
        //         trigger: 'blur',
        //     },],
    },

    getData,
    update: updateSearchKeyWord,
    create: createSearchKeyWord,
})





// const handleSizeChange = (val) => {
//   getData()
// }
const handleCurrentChange = (val) => {
  getData()
}

// 打开新tab重定向链接
const isChange = ref([])
const goLink = (row) => {
    

    let uri="#";

    let _hps = row.link.split('://')
    if (_hps[0] == 'http' || _hps[0] == 'https'){
        uri = row.link
    } else {
        uri = 'http://' + row.link
    }
    // document.getElementById("hi_a").click();

    
    // let id="hi_a"
    createSuperLabel(uri,row.id)

    isChange.value.push(row.id)
}

// 创建超链接，不会被拦截    
function createSuperLabel(url, id) {      
    let a = document.createElement("a");           
    a.setAttribute("href", url);      
    a.setAttribute("target", "_blank");      
    a.setAttribute("id", id);       
    // 防止反复添加      
    if(!document.getElementById(id)) {                               
        document.body.appendChild(a);      
    }      
    a.click();    
}




// const beforeChangeStatus = (row) => {
    
//     let content = row.status ? "是否取消锁定？" :  "是否锁定此网站,并且只允许自己取消锁定？" 
//     let title = row.status ? "打入冷宫？"  : "纳入后宫？"
    

//     return new Promise((resolve, reject) => {
//         showModal(content, "warning", title).then(()=> {
//                 resolve(true)
//             }).catch(() => {
//                 toast('已取消', 'info')
//                 reject(false)
//             })
//         })
// }



const handlerChangeStatus = (status,row) => {
    
    let is_contact = status
    row.statusLoading = true
    lockSearchKeyWord(row.id, is_contact).then((res)=>{
        if(status){
            // toast('<p>关键词: '+ row.owner.name + '</p>' +'<p>排名序号: '+ row.number  + '</p><p>网站网址：'+ row.url_website + '</p><p>执行人：'+ store.state.user.username +'</p><p style="margin-top: 20px;color: green;"><i class="el-icon" data-v-ea893728="" style="font-size: 20px;"><svg  viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" data-v-ea893728=""><path fill="currentColor" d="M224 448a32 32 0 0 0-32 32v384a32 32 0 0 0 32 32h576a32 32 0 0 0 32-32V480a32 32 0 0 0-32-32H224zm0-64h576a96 96 0 0 1 96 96v384a96 96 0 0 1-96 96H224a96 96 0 0 1-96-96V480a96 96 0 0 1 96-96z"></path><path fill="currentColor" d="M512 544a32 32 0 0 1 32 32v192a32 32 0 1 1-64 0V576a32 32 0 0 1 32-32zm192-160v-64a192 192 0 1 0-384 0v64h384zM512 64a256 256 0 0 1 256 256v128H256V320A256 256 0 0 1 512 64z"></path></svg></i>锁定成功</p>');
            toast('<p style="margin-top: 20px;color: green;"><i class="el-icon" data-v-ea893728="" style="font-size: 20px;"><svg  viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" data-v-ea893728=""><path fill="currentColor" d="M224 448a32 32 0 0 0-32 32v384a32 32 0 0 0 32 32h576a32 32 0 0 0 32-32V480a32 32 0 0 0-32-32H224zm0-64h576a96 96 0 0 1 96 96v384a96 96 0 0 1-96 96H224a96 96 0 0 1-96-96V480a96 96 0 0 1 96-96z"></path><path fill="currentColor" d="M512 544a32 32 0 0 1 32 32v192a32 32 0 1 1-64 0V576a32 32 0 0 1 32-32zm192-160v-64a192 192 0 1 0-384 0v64h384zM512 64a256 256 0 0 1 256 256v128H256V320A256 256 0 0 1 512 64z"></path></svg></i>锁定成功</p>', 'success',true, '400');
        } else {
            toast('<p style="margin-top: 20px;color: green;"><i class="el-icon" data-v-ea893728="" style="font-size: 20px;"><svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" data-v-ea893728=""><path fill="currentColor" d="M224 448a32 32 0 0 0-32 32v384a32 32 0 0 0 32 32h576a32 32 0 0 0 32-32V480a32 32 0 0 0-32-32H224zm0-64h576a96 96 0 0 1 96 96v384a96 96 0 0 1-96 96H224a96 96 0 0 1-96-96V480a96 96 0 0 1 96-96z"></path><path fill="currentColor" d="M512 544a32 32 0 0 1 32 32v192a32 32 0 1 1-64 0V576a32 32 0 0 1 32-32zm178.304-295.296A192.064 192.064 0 0 0 320 320v64h352l96 38.4V448H256V320a256 256 0 0 1 493.76-95.104l-59.456 23.808z"></path></svg></i><span class="icon-name" data-v-ea893728="">取消锁定</p>', 'success',true, '400');

        }
    }).finally(()=>{
        row.statusLoading = false
        getData()
    })

}






// 复制
const { toClipboard } = useClipboard();
    const copy = async (row) => {
    try {
        await toClipboard(row.owner.name);
        // toast('归属系列:'+ row.owner.name + '\n' +'下的渠道号:'+ row.channel_code + 'OP链接复制成功:');
        toast('<p style="margin-top: 10px;color: green;">复制成功</p>', 'success',true, '400');

    } catch (e) {
        toast('复制失败 || 关键词名称不存在','warning')
        console.error(e);
    }
};




// 导出替换某些字段
function fieldReplace(newDate) {
    
    newDate.forEach(e => {

        // console.log('循环E:',e)

        if(e.is_contact == 0) {
            e.is_contact = "未锁定"
        } else if (e.is_contact == 1) {
            e.is_contact = "已锁定"
        } else {
            e.is_contact = "未知"
        }

        
        // 如果存在关联
        if (e.owner) {
            if(e.owner_id == e.owner.id){
                e.owner =  e.owner.name
            }
        } else {
            e.owner =  '未知'
        }


        // // 标签 ID  替换成标签名称
        // let _tag_id = e.tag_id
        // let tags = []
        // _tag_id.forEach(t1 => {
            
        //     fromRemoteTags.value.forEach(t2 => {
        //         if(t1 == t2.id){
        //             tags.push(t2.name)
        //         }
        //     })
        // });
        // e.tags = tags.join(',')
    });

    return newDate
}
    
// 下载当页数据
const exportToExcel = ()=> {
    
    loading.value = true

    let newDate = fieldReplace(tableData.value)
    
    let fields = {
        owner: "关键词名称",
        number: "排名序号",
        link: "对应链接",
        url_website: "网站网址",
        contact: "联系方式",
        en: '类型',
        is_contact: "是否锁定",
        contact_user: "执行者",
        first_name: "导入者",
        last_name: "更新者",
        created_at: "创建时间",
        updated_at: "更新时间",
    };


    // let data = JSON.parse(JSON.stringify(this.tableData3));  // 如果直接放置数据不行请加上这句

    exportExcel(newDate, fields, getCurrentTime() + "_keyword");
    getData()

    loading.value = false
}


// // 条件下载
// const keywordName = ref(null)
// const formDialogRef = ref(null)
// const DialogTitle = ref(null)
// const conditionToExcel = () => {
//     let _asyncwd = []
//     searchForm.asynckeyword.forEach(e => {
//         existSearchs.value.map(o => {
//             // console.log(o.id, e)
//             if(o.id == e) {
//                 _asyncwd.push(o.name)
//             }
            
//         })
//     });
//     keywordName.value = _asyncwd

//     DialogTitle.value = '条件下载确认'
//     formDialogRef.value.open()
// }









const selectRemoteLoading  = ref(false)
const options = ref([])
const remoteMethod = (query) => {
    // console.log(query)
    if (query) {
        selectRemoteLoading.value = true

        searchKeyword({q: query, s: 1}).then(res=> {
            options.value = res
        }).finally(()=> {
            selectRemoteLoading.value = false
        })
        // setTimeout(() => {
        //     loading.value = false
        //     options.value = existSearchs.value.filter((item) => {
        //         return item.name.toLowerCase().includes(query.toLowerCase())
        //     })

        //     console.log(options.value)
        // }, 100)
    } else {
        options.value = []
    }
}



// 新增编辑时使用
const selectRemoteLoadingTwo  = ref(false)
const optionsTwo = ref([])
const editLoading = ref(false)
const remoteMethodTwo = (query) => {
    // console.log(query)
    if (query) {
        selectRemoteLoading.value = true

        searchKeyword({q: query}).then(res=> {
            optionsTwo.value = res
        }).finally(()=> {
            selectRemoteLoadingTwo.value = false
        })
    } else {
        optionsTwo.value = []
    }
}


// 点击编辑时获取当前ID数据
const handleEditBefore = (row) => {
    optionsTwo.value = []
    
    editLoading.value = true

    showSearchKeyWord(row.id).then(res => {
        optionsTwo.value.push(res.owner)
        handleEdit(row)
    }).finally(()=>{
        editLoading.value = false
    })
}



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


// // 解决 select 数据量大卡顿问题
// const optionsKeyWord = ref([])


// function selectChange (val) {
//     let _options = val.map(idx => ({
//         value: idx.id,
//         label:  idx.name,
//     }))

//     optionsKeyWord.value = _options

// }
// const handleCreateBefore = () => {

//     // let _options = []
//     // loading.value = true
//     // searchKeyword({q: query}).then(res=> {
//     //     _options = res
//     // }).finally(()=> {
//     //     loading.value = false
//     // })

//     selectChange()
//     handleCreate()
// }





// xTable 执行批量删除的操作
const xTableRef = ref(null)
const ids = ref([])
const handleSelectionChangeBefore = (val) => {
    const $table = xTableRef.value
    const selectRecords = $table.getCheckboxRecords()
    let _ids = []
    selectRecords.forEach(e => {
        _ids.push(e.id)
    });

    ids.value = _ids

    // console.log('选中ID,',_ids)
}

function handleMultiDelete () {
    loading.value = true
    batchDeleteSearchKeyWord(ids.value)
    .then(res => {
        toast(`批量删除数据成功`)
        getData()
    })
    .finally(()=> {
        loading.value = false
    })
}


onMounted(()=> {

    setTimeout(() => {
        getSearchKeyWordGroupByNumber().then(res => {
            numbers.value = res.numbers
        })
    },50)

    // setTimeout(() => {
    //     getSearchKeyWordGroupByUser().then(res => {
    //         first_names.value = res.first_names
    //     })
    // },100)


    setTimeout(() => {
        getSearchKeyWordGroupBy().then(res=> {

            existSearchs.value = res.existSearchs
            keywords.value = res.keywords
            // numbers.value = res.numbers
            is_locks.value = res.is_locks
            contact_users.value = res.contact_users
            first_names.value = res.first_names
            last_names.value = res.last_names
            ens.value = res.ens
            colors.value = res.colors
            types.value = res.types
            is_contacts.value = res.is_contacts
            
        })
    }, 150)
      
})



// 批量锁定
const handleBatchLock = () => {
    if (ids.value.length == 0) {
        toast('无数据锁定','warning')
        return false
    }
    loading.value = true
    batchLockSearchKeyWord(ids.value)
    .then(res=> {
        toast('锁定成功')
        ids.value = []
        getData()
    })
    .finally(()=>{
        loading.value = false
    })
}






// 条件下载
const keywordName = ref(null)
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
    getSearchKeyWordList(searchForm).then(async res => {
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

// 进度条
const task_id = ref(null)
const timerLoading = ref(null)
const progresscolors = [
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


<style>
.el-popper.is-customized {
  /* Set padding to ensure the height is 32px */
  padding: 6px 12px;
  background: linear-gradient(90deg, rgb(159, 229, 151), rgb(204, 229, 129));
}

.el-popper.is-customized .el-popper__arrow::before {
  background: linear-gradient(45deg, #b2e68d, #bce689);
  right: 0;
}

.act {
    background-color: red;
}









/* 测试样式 */
        /*滚动条整体部分*/
        .mytable-scrollbar ::-webkit-scrollbar {
          width: 10px;
          height: 10px;
        }
        /*滚动条的轨道*/
        .mytable-scrollbar ::-webkit-scrollbar-track {
          background-color: #FFFFFF;
        }
        /*滚动条里面的小方块，能向上向下移动*/
        .mytable-scrollbar ::-webkit-scrollbar-thumb {
          background-color: #bfbfbf;
          border-radius: 5px;
          border: 1px solid #F1F1F1;
          box-shadow: inset 0 0 6px rgba(0,0,0,.3);
        }
        .mytable-scrollbar ::-webkit-scrollbar-thumb:hover {
          background-color: #A8A8A8;
        }
        .mytable-scrollbar ::-webkit-scrollbar-thumb:active {
          background-color: #787878;
        }
        /*边角，即两个滚动条的交汇处*/
        .mytable-scrollbar ::-webkit-scrollbar-corner {
          background-color: #FFFFFF;
        }
        
</style>