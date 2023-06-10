<template>
    <el-card shadow="always" class="border-0">

        <!-- 搜索 -->
        <Search @model="searchForm" @search="getData" @reset="resetSearchFrom">


            <SearchItem label="搜索">
                <el-input v-model="searchForm.keyword" placeholder="会员ID、姓名、银行卡号" clearable @keyup.enter="getData" v-on:input="getData"></el-input>
            </SearchItem>


            <!-- 添加到自定义插槽 -->
            <template #show>

                <SearchItem label="所属部门">
                    <el-select v-model="searchForm.owner_id"   placeholder="" clearable filterable >
                        <el-option v-for="(item, index) in groups"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
                            >
                        </el-option>
                    </el-select>
                </SearchItem>


                <SearchItem label="申请日期">

                <el-date-picker
                    v-model="searchForm.start"
                    type="date"
                    placeholder="请选择申请日期"
                    size="small"
                    format="YYYY-MM-DD"
                    value-format="YYYY-MM-DD"
                />
                </SearchItem>

                <SearchItem label="操作日期">

                <el-date-picker
                    v-model="searchForm.end"
                    type="date"
                    placeholder="请选择操作日期"
                    size="small"
                    format="YYYY-MM-DD"
                    value-format="YYYY-MM-DD"
                />
                </SearchItem>




                <SearchItem label="申请人">
                    <el-select v-model="searchForm.first_name"  placeholder="" clearable filterable>
                        <el-option v-for="(item, index)  in f_users"
                            :key="item.first_name"
                            :label="item.first_name"
                            :value="item.first_name"
                            >
                        </el-option>
                    </el-select>
                </SearchItem>

            
                    
                <SearchItem label="接单员">
                    <el-select v-model="searchForm.last_name"  placeholder="" clearable filterable>
                        <el-option v-for="(item, index)  in l_users"
                            :key="item.last_name"
                            :label="item.last_name"
                            :value="item.last_name"
                            
                            >
                        </el-option>
                    </el-select>
                </SearchItem>


                <SearchItem label="接单状态">
                    <el-select v-model="searchForm.rece_id"  placeholder="" clearable filterable>
                        <el-option v-for="(item, index)  in searchReces"
                            :key="item.id"
                            :label="item.label"
                            :value="item.id"
                            >
                        </el-option>
                    </el-select>
                </SearchItem>





            </template>
        </Search> 


        

        <ListHeader :Interval="true"  layout="refresh"    @refresh="getData">
        
            <el-button type="primary" size="small" @click="handleCreate" v-permission="['CreateRecordOutMoney,POST']"><el-icon><Plus /></el-icon> 新增</el-button>
            <el-popconfirm
                title="是否要批量彻底删除选择的记录,不可逆操作"
                confirmButtonText="确认"
                cancelButtonText="取消"
                confirmButtonType="primary"
                @confirm="handleMultiDelete">
                <template #reference>
                    <el-button type="danger" size="small" v-permission="['DeleteBatchRecordOutMoney,POST']"><el-icon><Delete /></el-icon> 批量删除</el-button>
                </template>
            </el-popconfirm>
        
        </ListHeader>
  
        <!-- 表格 -->
        <vxe-table
            border
            max-height="800"
            show-overflow
            show-footer
            :footer-method="footerMethod"
            keep-source
            ref="multipleTableRef"
            :data="tableData"
            class="mytable-scrollbar mytable-style"
            header-align="center" 
            style="width: 100%; font-size: 1vh; height: 100%;"  
            :loading="loading" 
            :cell-class-name="cellClassName"
            @checkbox-all="handleSelectionChangeEvent"
            @checkbox-change="handleSelectionChangeEvent" 

            :row-config="{isCurrent: true, isHover: true}"
            :sort-config="{chronological: true, remote: true}"
            @sort-change="SortVxeChangeEvent"

            :edit-config="{trigger: 'click', mode: 'cell', showStatus: true}"
            @edit-closed="editClosedEvent"
            v-permission="['getListRecordOutMoney,GET']"
            >


            <vxe-column type="checkbox" align="center"  width="3%"></vxe-column>
            <vxe-column title="归属"    align="center"  width="5%">
                <template  #default="{ row }">
                    <span>{{ row.owner ? row.owner.name : '-' }}</span>
                </template>
            </vxe-column>
            <vxe-column field="uid" title="会员ID"   align="center" width="6%"/>
            <vxe-column field="bank_name" title="会员姓名"   align="center" width="6%"/>
            <vxe-column field="bank_owner" title="所属银行"   align="center" width="6%"/>
            <vxe-column field="bank_child" title="支行"   align="center" width="13%"/>
            <vxe-column field="bank_card" title="银行卡号"   align="center" width="10%"/>
            <vxe-column field="out_money" title="出款金额"   align="center" width="6%">
                <template #default="{ row }">
                    ¥: {{ row.out_money ? row.out_money : 0 }}
                </template>
            </vxe-column>

            <vxe-column field="two_enter" title="信息核对"   align="center" width="6%">
                <template #default="{ row }">
                    <!-- {{ row.two_enter ? "已确认" : "未确认" }} -->
                    <el-steps :space="200" :active="1" finish-status="success" v-if="row.two_enter">
                        <el-step/>
                    </el-steps>

                    <el-button
                        type="warning"
                        size="small"
                        round
                        @click="handlerTwoEnter(row)"
                        v-permission="['CreateRecordOutMoney,POST']"
                        v-else
                    >
                    二次确认  
                    </el-button>

                    <el-tag type="warning" v-permission="['ReceRecordOutMoney,POST']" v-if="row.two_enter == 0">等待确认</el-tag>

                    <!-- <el-steps :space="200" :active="1" finish-status="error" v-else>
                        <el-step/>
                    </el-steps> -->
                    
                    
    
                </template>
            </vxe-column>



            <vxe-column field="img_path" title="截图" align="center"  width="10%">
                <template #default="{row, rowIndex}">
                    <div class="flex justify-center imgStyle" v-if="row.img_path && row.two_enter == 1 && row.rece_state == 2 || row.rece_state == 3">
                        <ul class="qoweuqwe" v-for="(item,index) in row.img_path" :key="index">
                            <li>
                                <el-popover
                                    placement="right"
                                    trigger="click"
                                    width="400"
                                    >
                                    <img :src="'api/' + item" alt=""/>
                                    <template #reference>
                                        <el-image :src="'api/' + item"  fit="fill" :lazy="true" style="padding:  5px; " v-if="row.img_path.length == 1"></el-image>
                                        <el-image :src="'api/' + item"  fit="fill" :lazy="true" style="max-height: 80px; max-width: 80px;padding:  5px; " v-if="row.img_path.length == 2"></el-image>
                                        <el-image :src="'api/' + item"  fit="fill" :lazy="true" style="max-height: 80px; max-width: 80px;padding:  2px; " v-if="row.img_path.length == 3"></el-image>
                                        <el-image :src="'api/' + item"  fit="fill" :lazy="true" style="max-height: 70px; max-width: 70px;padding:  2px; " v-if="row.img_path.length == 4"></el-image>
                                        <el-image :src="'api/' + item"  fit="fill" :lazy="true" style="max-height: 35px; max-width: 35px;padding:  2px; " v-if="row.img_path.length > 4"></el-image>
                                    </template>
                                </el-popover>

                                
                            </li>
                        </ul>
                    </div>

                    
                    <el-button type="info" size="small" @click="openUploadFile(row)" v-permission="['ReceRecordOutMoney,POST']" v-if="row.two_enter == 1 && row.rece_state == 1 && $store.state.user.username == row.last_name"><el-icon><Upload /></el-icon>上传</el-button>
                </template>
            </vxe-column>
            <vxe-column field="description" title="备注"    align="center" width="10%"  :edit-render="{}">
                <template #edit="{ row }">
                    <vxe-input v-model="row.description" type="text" placeholder="输入备注" v-if="$store.state.user.username == row.last_name"></vxe-input>
                    <vxe-input v-model="row.description" type="text" placeholder="输入备注" disabled v-else></vxe-input>
                </template>
            </vxe-column>
            <vxe-column field="first_name" title="申请人"   align="center" width="4%"/>
            <vxe-column field="last_name" title="接单员"    align="center" width="4%"/>
            



            


            <vxe-column field="created_at"  title="申请时间" align="center" sortable  width="9%">
                <template  #default="{ row }">
                    <span>{{ row.created_at ? dateFormat(row.created_at) : '' }}</span>
                </template>
            </vxe-column>

            <vxe-column  field="updated_at" title="操作时间" align="center" sortable  width="9%">
                <template  #default="{ row }">
                    <span>{{ row.updated_at ? dateFormat(row.updated_at) : ''  }}</span>
                </template>
            </vxe-column>




            <vxe-column  title="操作" fixed="right" width="7%">
                <template #default="{ row }">
                    <el-button 
                        size="small" 
                        :icon="Edit"
                        @click="handleEdit(row)"
                        v-permission="['UpdateRecordOutMoney,PUT']"
                        v-if="row.two_enter == 0"
                    /> 

                    <el-popconfirm
                        title="是否要删除该记录"
                        confirmButtonText="确认"
                        cancelButtonText="取消"
                        confirmButtonType="primary"
                        @confirm="handleDelete(row.id)"
                        v-if="row.two_enter == 0"
                        >
                        <template #reference>
                            <el-button size="small" :icon="Delete" type="danger" v-permission="['DeleteRecordOutMoney,DELETE']" />
                        </template>
                    </el-popconfirm>

                    <el-button 
                        size="small" 
                        :icon="Edit"
                        @click="handleReceState(row)"
                        v-if="row.two_enter == 1 && row.rece_state == 0"
                        v-permission="['ReceRecordOutMoney,POST']"
                    > 
                    立马接单
                    </el-button>

                    <el-tag type="danger" size="small"  v-permission="['CreateRecordOutMoney,POST','ReceRecordOutMoney,POST']" v-if="row.two_enter == 1 && row.rece_state == 0"><el-icon><Van /></el-icon>正在派送中</el-tag>
                    <el-tag type="warning" size="small" v-permission="['CreateRecordOutMoney,POST','ReceRecordOutMoney,POST']" v-if="row.two_enter == 1 && row.rece_state == 1"><el-icon class="is-loading rececolor"><Loading /></el-icon>正在处理中</el-tag>
                    <el-tag type="success" size="small" v-permission="['CreateRecordOutMoney,POST','ReceRecordOutMoney,POST']" v-if="row.two_enter == 1 && row.rece_state == 2"><el-icon><SuccessFilled /></el-icon>此单已支付</el-tag>
                    <el-tag type="danger" size="small"  v-permission="['CreateRecordOutMoney,POST','ReceRecordOutMoney,POST']" v-if="row.two_enter == 1 && row.rece_state == 3"><el-icon><CloseBold /></el-icon>此单已作废</el-tag>


                    
                </template>
            </vxe-column>

            
          </vxe-table>

          <!-- 分页 -->
        <vxe-pager
            :layouts="['Sizes', 'PrevJump', 'PrevPage', 'Number', 'NextPage', 'NextJump', 'FullJump', 'Total']"
            :pageSizes="[10, 50, 200, 500, 1000, 5000]"
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


        <!-- 新增和修改 -->
        <FormDrawer ref="formDrawerRef" :title="drawerTitle"  @submit="handleSubmit">
            <el-form :model="form" ref="formRef" :rules="rules" label-width="80px" >


                <el-form-item label="所属部门" prop="owner_id">
                    <el-select v-model="form.owner_id"  style="width: 100%"   placeholder="" clearable filterable >
                        <el-option v-for="(item, index) in groups"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
                            >
                        </el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="会员ID" prop="uid">
                    <el-input v-model.trim="form.uid"  placeholder="会员ID"></el-input>
                </el-form-item>

                <el-form-item label="会员姓名" prop="bank_name">
                    <el-input v-model.trim="form.bank_name"  placeholder="会员姓名"></el-input>
                </el-form-item>

                <el-form-item label="所属银行" prop="bank_owner">
                    <el-input v-model.trim="form.bank_owner"  placeholder="所属银行"></el-input>
                </el-form-item>
                
                <el-form-item label="支行" prop="bank_child">
                    <el-input v-model.trim="form.bank_child"  placeholder="支行"></el-input>
                </el-form-item>

                <el-form-item label="银行卡号" prop="bank_card">
                    <el-input v-model.trim="form.bank_card"  placeholder="银行卡号"></el-input>
                </el-form-item>


                <el-form-item label="出款金额" prop="out_money"  >
                    <!-- <el-input v-model.trim="form.out_money"  placeholder="出款金额" type="number" oninput="if(isNaN(value)) { value = parseFloat(value) } if(value.indexOf('.')>0){value=value.slice(0,value.indexOf('.')+3)}"></el-input> -->
                    <el-input v-model.trim="form.out_money"  placeholder="出款金额,只支持小数点后跟两位" oninput="value=value.replace(/[^0-9.]/g,'')"></el-input>
                </el-form-item>



                
            </el-form>
        </FormDrawer>





                <!-- 上传 -->
        <el-drawer title="文件上传" v-model="drawer" size="30%">

            <el-input type="textarea" v-model="copyfile" :row="3" placeholder="点这里, ctrl + v 粘贴图片即上传"   @paste.native="handlePaste" class="mb-3"></el-input>
            
            <!-- <UploadFile :action="uploadImageAction" :data="{ id: img_id }" :multiple="false" @success="UploadSuccess"  v-if="uploadForm.img_path == ''"/> -->
            <el-upload
                v-model:file-list="fileList"
                :action="uploadImageAction"
                :headers="{
                    'X-Token': token
                }"
                multiple
                :data="{ id: img_id }"
                name="img"
                list-type="picture-card"
                :on-preview="handlePictureCardPreview"
                :on-remove="handleRemove"
                :on-success="uploadSuccess"
                :on-error="uploadError"
                >
                <el-icon><Plus /></el-icon>
            </el-upload>

            <!-- <el-dialog :visible.sync="dialogVisible">
                <img width="100%" :src="dialogImageUrl" alt="">
            </el-dialog> -->

                <p>部门: {{ p_show.owner.name }}</p>
                <p>会员账号：{{ p_show.uid}}</p>
                <p>会员姓名：{{ p_show.bank_name }}</p>
                <p>所属银行：{{ p_show.bank_owner }}</p>
                <p>支行：{{ p_show.bank_child }}</p>
                <p>银行卡号：{{ p_show.bank_card }}</p>
                <p>申请金额：{{ p_show.out_money }}</p>

            <el-form :model="uploadForm" ref="uploadFormRef" :rules="uploadRules" label-width="80px" >
                <!-- <el-form-item  label="截图" prop="img_path"> -->
                    <!-- <el-image style="width: 30%; height: 60%"  :src="'api/' + uploadForm.img_path"  @click.prevent="handlePictureCardPreview(uploadForm)"/> -->
                    <!-- <el-input v-model.trim="uploadForm.img_path"  placeholder="图片路径"></el-input> -->
                <!-- </el-form-item> -->
                <el-form-item label="备注" prop="description">
                    <el-input v-model.trim="uploadForm.description"  placeholder="备注"></el-input>
                </el-form-item>

                <el-form-item label="订单状态" prop="rece">
                    <el-select v-model="uploadForm.rece"  style="width: 100%"   placeholder="" clearable filterable >
                        <el-option v-for="(item, index) in reces"
                            :key="item.id"
                            :label="item.label"
                            :value="item.id"
                            >
                        </el-option>
                    </el-select>
                </el-form-item>
                
            </el-form>

            <el-button type="primary" size="default" @click="handleDone" style="width: 100%;">确认提交</el-button>
            
        </el-drawer>



        <!-- 点击放大图片 -->
        <el-dialog v-model="dialogVisible">
            <img w-full :src="dialogImageUrl" alt="Preview Image" />
        </el-dialog>
        

    </el-card>
</template>





<script setup>
import { ref,onMounted, reactive,watchEffect,onDeactivated } from 'vue'
import {  Delete, Edit } from '@element-plus/icons-vue'
import Search from '@/components/Search.vue'
import SearchItem from '@/components/SearchItem.vue'
import UploadFile from '@/components/UploadFile.vue'
import FormDialog from '@/components/FormDialog.vue'
import store from '@/store'

import { 
    getListRecordOutMoney,
    createRecordOutMoney,
    updateRecordOutMoney,
    deleteRecordOutMoney,
    statusRecordOutMoney,
    receRecordOutMoney,
    doneRecordOutMoney,
    uploadImageAction,
    pasteUploadImage,
    descRecordOutMoney,
    DeletebatchRecordOutMoney
    
} from "@/api/recordOutMoney.js"

import ListHeader from '@/components/ListHeader.vue';
import FormDrawer from '@/components/FormDrawer.vue';
import { useInitTable,useInitForm } from '@/composables/useCommon'
import { dateFormat,toast,getNextDate,getCurrentTime } from '@/utils/tools.js'
import { getToken } from "@/utils/cookies"

const groups = ref([])
const f_users = ref([])
const l_users = ref([])
const srcList = ref([])
const reces = ref([])
const searchReces = ref([])
const dialogImageUrl = ref('')
const dialogVisible = ref(false)
const token = getToken()


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
    // handleSelectionChange,
    // handleStatusChange
} = useInitTable({
    searchForm: {
        asynckeyword: '',
        keyword: '',
        skip: 1,
        limit: 10,
        rece_id: '',
        first_name: '',
        last_name: '',
        start: '',
        end: '',
        paging: 1,
        field: '',
        order_by: '',
        owner_id: '',


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
            groups.value = res.groups
            f_users.value = res.f_users
            l_users.value = res.l_users
            reces.value = res.reces
            searchReces.value = res.searchReces


            res.list.map(o=>{
                if (o.img_path) {
                    // 分割
                    let _new = o.img_path.split(',')
                    _new.forEach(e => {
                        e = "api/" + e
                    });
                    o.img_path = _new
                } else {
                    o.img_path = ["api/"]
                }
                
                // _s.push('api/' + o.img_path)
                // if (o.img_path) {
                //     o.img_path = _new
                // } else {
                //     o.img_path = []
                // }
            })

            console.log(res.list)
            // srcList.value = _s
            // is_locks.value = res.is_locks
            // contact_users.value = res.contact_users
            // first_names.value = res.first_names
            // last_names.value = res.last_names
        },


    getList: getListRecordOutMoney,
    delete: deleteRecordOutMoney,
    multidelete: DeletebatchRecordOutMoney,
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
        owner_id: '',
        uid: '',
        bank_name:'',
        bank_owner: '',
        bank_child: '',
        bank_card: '',
        out_money: '',
    },
    rules: {
        owner_id: [{
                required: true,
                message: '归属部门不能为空',
                trigger: 'blur',
            },],
        uid: [{
                required: true,
                message: '会员ID不能为空',
                trigger: 'blur',
            },],
        bank_name: [{
                required: true,
                message: '会员姓名不能为空',
                trigger: 'blur',
            },],
        bank_owner: [{
                required: true,
                message: '所属银行不能为空',
                trigger: 'blur',
            },],
        bank_card: [{
                required: true,
                message: '银行卡号不能为空',
                trigger: 'blur',
            },],
        out_money: [{
                required: true,
                message: '出款金额不能为空',
                trigger: 'blur',
            },],
    },

    getData,
    update: updateRecordOutMoney,
    create: createRecordOutMoney,
})




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

const handleCurrentChange = (val) => {
  getData()
}













// 导入
const drawer = ref(false)
const upload = ref(null)
const importTitle = ref(null)
const importModel = ref(false)
const ImportFromExcelJson = ref([])
const excelDataLength = ref(0)
const successTotal = ref(0)
const updateTotal = ref(0)
const errorTotal = ref(0)
const errorData = ref([])
const task_id = ref(null)
const imageUrl = ref('')
const img_id = ref(0)
const p_show = ref(null)
const temp_list = ref([])
const fileList = ref([])
const uploadFormRef = ref(null)

const uploadForm = reactive({
    img_path : "",
    description: "",
    rece: ''
})

// 定义验证规则
const uploadRules = {
    rece: [
        {
            required: true,
            message: '订单状态必须选择',
            trigger: 'blur',
        },
    ],
}


// 打开上传文件
const openUploadFile = (row)=> {
    p_show.value = row
    img_id.value = row.id
    drawer.value = true
    uploadForm["img_path"]  = ""
}


// 上传成功触发
const uploadSuccess = (response, uploadFile, uploadFiles) => {

    toast(uploadFile.name + ' 上传成功')
    temp_list.value.push(uploadFile.response.data.path)
}

// 上传失败触发
const uploadError =(error, uploadFile, uploadFiles)=>{
  let msg = JSON.parse(error.message).msg || "上传失败"
  toast(msg,"error")
}

// 移除触发
const handleRemove = (file, fileList) =>  {
    let name = file.name
    let path = file.response.data.path
    let index = temp_list.value.indexOf(path)
    temp_list.value.splice(index, 1)
    toast('移除图片 ' + name)
}



// 点击图片触发
const handlePictureCardPreview = (uploadFile) => {
    
    if (uploadFile.response) {
        dialogImageUrl.value = "api/" + uploadFile.response.data.path
    } else {
        dialogImageUrl.value =  uploadFile.url
    }
    
    dialogVisible.value = true
}


// 点击触发图片数据保存，并结单
const handleDone = () => {

    uploadFormRef.value.validate((valid) => {
        if (!valid) {
            console.log('error')
            return false;
        }

        uploadForm['img_path'] = temp_list.value.join(',')
        loading.value = true
        doneRecordOutMoney(p_show.value.id, uploadForm).then(res=>{
            drawer.value = false
            // p_show.value = null
            img_id.value = 0
            uploadFormRef.value.resetFields()
            fileList.value = []
            temp_list.value = []
            getData()
        })
        .finally(()=>{
            loading.value = false
        })

    })



}


// 上传成功触发
// const UploadSuccess = (response, uploadFile, uploadFiles) => {
//     uploadForm["img_path"] = response.response.data.path
//     // console.log("获取值",res)
//     // img_id.value = 0
//     // drawer.value = false

//     console.log(uploadForm)
//     // getData()s
// }



// const handleAvatarSuccess = (response, uploadFile) => {
//   imageUrl.value = URL.createObjectURL(!uploadFile.raw)
// }

// const beforeAvatarUpload = (rawFile) => {
//   if (rawFile.type !== 'image/jpeg') {
//     toast('上传图片只能是 png、jpg格式!', 'warning')
//     return false
//   } else if (rawFile.size / 1024 / 1024 > 2) {
//     toast('上传图片大小不能超过 2MB!', 'warning')
//     return false
//   }
//   return true
// }



// // 上传图片触发
// const UploadOnChange = (e) => {
//     console.log(e)
//     const TYPE = ['png', 'jpg']
//     const extension = TYPE.includes(e.name.split('.')[1])
//     const isLt2M = e.size / 1024 / 1024 < 2

//     if (!extension) {
//         toast('上传图片只能是 png、jpg格式!', 'warning')
//         upload.value.clearFiles()
//         return false
//     }

//     if (!isLt2M) {
//         toast('上传图片大小不能超过 2MB!', 'warning')
//         upload.value.clearFiles()
//         return false
//     }

//     imageUrl.value = e.name
//     return true
// }




// // 移除上传文件触发
// const UploadRemove = async (ev) => {
//     toast(`移除文件: ${ ev.name}`, 'info')
// }

// // 上传文件超出限制触发
// const UploadExceed = async (ev) => {
//     toast('超出上传文件最大限制,请先移除已有 EXCEL 文件', 'warning')
// }

// // 点击上传触发
// const handleImport = async () => {
//     toast('上传成功')
// }


// 挂载
onMounted(() => {
    // setTimeout(()=> {
    //     getMemberCaiJinSourceList({paging: 0}).then(res=>{
    //         sources.value = res.list
    //     })
    // }, 100)

    
})


// 信息核对
const handlerTwoEnter = (row) => {
    statusRecordOutMoney({id: row.id, status: 1})
    .then((res)=>{
        toast('二次确认成功')
        getData()
    })
}


// 点击备注实时保存
// const xTableRef = ref(null)
const editClosedEvent = ({ row, column }) => {
    const $table = multipleTableRef.value
    const field = column.field
    const cellValue = row[field]

    // 判断单元格值是否被修改
    if ($table.isUpdateByRow(row, field)) {



        descRecordOutMoney(row.id, row.description).then(res=>{
            toast(`备注修改成功！`)
            // 局部更新单元格为已保存状态
            $table.reloadRow(row, null, field)
        })
    }
}


// 点击接单
const handleReceState = (row) => {
    loading.value = true
    receRecordOutMoney(row.id).then(res=>{
        toast('接单成功,请尽快安排支付并上传图片')
        getData()
    })
    .finally(()=>{
        loading.value = false
    })
}






// 当页金额计算
const sumNum = (list, field) => {
    let count = 0
    list.forEach(item => {
        count += Number(item[field])
    })
    return count
}

const footerMethod = ({ columns, data }) => {
    // console.log(columns)
    // console.log('数据', data)
    
    const footerData = [
    columns.map((column, columnIndex) => {
        if (columnIndex === 6) {
            return '合计'
        }
        if (['out_money'].includes(column.field)) {
            return '¥: ' + sumNum(data, column.field)
        }

        
        return null
        })
    ]


    return footerData
}

const  cellClassName = ({ row, column }) => {
    if (column.field === 'img_path') {
        return 'col-red'
    }
    return null
}


// 粘贴图片上传触发
const copyfile = ref(null)
const  handlePaste = (value) => {
    let items = value.clipboardData.items[0]
    if(items.type.includes('image')) {
        let imgfile = items.getAsFile()
        const formData = new FormData()
        formData.append('img', imgfile)
        formData.append('id', img_id.value)
        pasteUploadImage(formData).then(res=> {
            console.log(fileList.value)

            // 展示使用
            fileList.value.push({
                "name": "asdf",
                "url": 'api/' + res.path,
                "response": { "data": res }
            })
            // 传给接口使用
            temp_list.value.push(res.path)
        })
        
        
    }
}



</script>


<style>

.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}


.rececolor {
    color: red !important;
}



.imgStyle {
    overflow: scroll;
    overflow-x: scroll;
    text-align: center;
}


.qoweuqwe li{
    display: block;
    float: left;
}



/* .imgStyle::-webkit-scrollbar{
  width: 4px;
  height: 4px;
}

.imgStyle::-webkit-scrollbar-corner{
  display: block;
}

.imgStyle::-webkit-scrollbar-thumb{
  border-radius: 8px;
  background-color: rgba(0, 0, 0, 0.2);
}

.imgStyle::-webkit-scrollbar-track{
  border-right-color: transparent;
  border-left-color: transparent;
  background-color: rgba(0, 0, 0, 0.1);
} */


</style>