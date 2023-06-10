<template>
    <div>
        <el-card shadow="always" class="border-0">
    
            <!-- 搜索 -->
            <Search @model="searchForm" @search="getData" @reset="resetSearchFrom">
                <SearchItem label="搜索">
                    <el-input v-model="searchForm.keyword" placeholder="渠道号、账号、ID、姓名、银行、电话、备注" clearable @keyup.enter="getData" v-on:input="getData"></el-input>
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
    
                    <SearchItem label="标签">
                        <el-select v-model="searchForm.owner_tag_id"  multiple placeholder="" clearable filterable >
                            <el-option v-for="(item, index)  in fromRemoteTags"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id">
                            </el-option>
                        </el-select>
                    </SearchItem>
                    

                    <SearchItem label="导入者">
                        <el-select v-model="searchForm.first_name"  placeholder="" clearable filterable style="width: 40vh;">
                            <el-option v-for="(item, index)  in users"
                                :key="item"
                                :label="item"
                                :value="item"
                                >
                            </el-option>
                        </el-select>
                    </SearchItem>



                    
                <SearchItem label="更新者">
                    <el-select v-model="searchForm.last_name"  placeholder="" clearable filterable>
                        <el-option v-for="(item, index)  in users"
                            :key="item"
                            :label="item"
                            :value="item"
                            >
                        </el-option>
                    </el-select>
                </SearchItem>



                <!-- <SearchItem label="创建时间">

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
                </SearchItem> -->




                </template>
            </Search>


            <!-- 进度条 -->
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

        
            <ListHeader layout="refresh,download,condition"  @download="exportToExcel" @condition="conditionToExcel" @refresh="getData" >
                <el-button type="primary" size="small" @click="handleCreate"  v-permission="['createMemberProfile,POST']"><el-icon><Plus /></el-icon> 新增</el-button>
                <!-- <el-button type="info" plain size="small" @click="handleBatchSearch"   v-permission="['multiSearchMember,POST']"><el-icon><Aim /></el-icon> 批量搜索</el-button>
                <el-button type="warning" plain size="small" @click="handleBatchModify"     v-permission="['multiModifyMember,POST']"><el-icon><EditPen /></el-icon> 批量修改</el-button> -->
    
                <!-- <el-popconfirm
                    title="是否要批量删除选择的记录,可在回收站恢复"
                    confirmButtonText="确认"
                    cancelButtonText="取消"
                    confirmButtonType="primary"
                    @confirm="handleMultiDelete">
                    <template #reference>
                        <el-button type="danger" size="small" v-permission="['multideleteMember,POST']"><el-icon><ShoppingCart /></el-icon> 批量删除</el-button>
                    </template>
                </el-popconfirm> -->
    
    
                
                <el-button  plain size="small"  @click="openUploadFile"   v-permission="['importExcelMemberProfile,POST']"><el-icon><Upload /></el-icon> 文件上传</el-button>
  
    
            </ListHeader>
    
                <!-- 表格 -->
                <vxe-table
                    border
                    max-height="800"
                    :column-config="{resizable: true}"
                    :data="tableData"
                    :loading="loading" 
                    ref="multipleTableRef"
                    class="mytable-scrollbar"
                    header-align="center" 
                    style="width: 100%; font-size: 1vh; height: 100%;"  
                    @checkbox-all="handleSelectionChangeEvent"
                    @checkbox-change="handleSelectionChangeEvent" 
    
                    :row-config="{isCurrent: true, isHover: true}"
                    :sort-config="{chronological: true, remote: true}"
                    @sort-change="SortVxeChangeEvent"
                    v-permission="['getListMemberProfile,GET']"
                >
    
                <vxe-column type="checkbox" align="center" fixed="left" width="2%"></vxe-column>
                <vxe-column title="归属部门" fixed="left"   align="center"  width="6%">
                    <template  #default="{ row }">
                        <span>{{ row.owner_id ? row.owner.name: '-' }}</span>
                    </template>
                </vxe-column>
    
                <vxe-column field="code"  title="渠道号" width="8%" align="center"/>

    
    
                
                <vxe-column field="account"  title="会员账号"   align="center" width="9%" ></vxe-column>
                <vxe-column field="account_id"  title="游戏ID"   align="center" width="9%" ></vxe-column>
                <vxe-column field="realname"  title="真实姓名"   align="center" width="9%" ></vxe-column>
                <vxe-column field="contact"  title="所属银行"   align="center" width="9%" ></vxe-column>
                <vxe-column field="bank_number"  title="绑定银行卡号"   align="center" width="10%" show-overflow="ellipsis"></vxe-column>
                <vxe-column field="iphone_num"  title="联系方式"   align="center" width="6%" show-overflow="ellipsis"></vxe-column>

                 
    
                <vxe-column title="标签" width="8%" align="center">
                    <template  #default="{ row }">
                        <span v-for="(item, index) in row.tags" :key="index"> 
                            <el-tag class="ml-2"   :color="item.color" effect="light" style="color: #fff !important;">{{ item.name }}</el-tag>
                        </span>
                    </template>
                </vxe-column>


                <vxe-column field="description" title="备注" width="9%" align="center" show-overflow="ellipsis"/>
                <vxe-column field="first_name"  title="创建者" width="5%" align="center"/>
                <vxe-column field="last_name"   title="更新者" width="5%" align="center"/>
    
                <vxe-column field="created_at"  title="创建时间" width="9%" align="center" sortable>
                    <template  #default="{ row }">
                        <span>{{ row.created_at ? dateFormat(row.created_at) : '' }}</span>
                    </template>
                </vxe-column>
    
                <vxe-column field="updated_at"  title="更新时间" width="9%" align="center" sortable>
                    <template  #default="{ row }">
                        <span>{{ row.updated_at ? dateFormat(row.updated_at) : '' }}</span>
                    </template>
                </vxe-column>
    
    
    
                <vxe-column title="操作" fixed="right" width="7%" align="center" v-if="searchForm.tab != 'delete'">
                    <template #default="scope">
    
                        <el-button 
                            size="small" 
                            :icon="Edit"
                            @click="handleEdit(scope.row)"
                            v-permission="['updateMemberProfile,PUT']"
                        /> 
    
                        <el-popconfirm
                            title="是否要删除该记录"
                            confirmButtonText="确认"
                            cancelButtonText="取消"
                            confirmButtonType="primary"
                            @confirm="handleDelete(scope.row.id)"
                            >
                            <template #reference>
                                <el-button size="small" :icon="Delete" type="danger" v-permission="['deleteMemberProfile,DELETE']"/>
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
                @page-change="handleCurrentChange"
                v-if="hiddlePage"
                >
    
                <template #right>
                    <div class="flex justify-between justify-center">
                        <img src="@/assets/img/89fc-fyscsmv5911424.gif" height="10" width="30">
                    <img src="@/assets/img/89fc-fyscsmv5911424.gif" height="10" width="30">
                    <img src="@/assets/img/89fc-fyscsmv5911424.gif" height="10" width="30">
                    </div>
                    
              </template>
            </vxe-pager>
    
            
    
            <!-- 新增和修改 -->
            <FormDrawer ref="formDrawerRef" :title="drawerTitle" size="60%" @submit="handleSubmit">
                <el-form :model="form" ref="formRef" :rules="rules" label-width="140px" >
    
                    
                    <el-form-item label="归属部门" prop="owner_id">
                        <el-select v-model="form.owner_id"  style="width: 100%" placeholder="选择所属部门">
                            <el-option v-for="item in groups"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
    
   
    
                    <el-form-item label="渠道号" prop="code"  >
                        <el-input v-model.trim="form.code"  placeholder="渠道号"></el-input>
                    </el-form-item>
                    
                    <el-form-item label="会员账号" prop="account">
                        <el-input v-model.trim="form.account"  placeholder="会员账号"></el-input>
                    </el-form-item>

                    <el-form-item label="游戏ID" prop="account_id">
                        <el-input v-model.trim="form.account_id"  placeholder="游戏ID"></el-input>
                    </el-form-item>
    
                    <el-divider />
    


                    <el-form-item label="真实姓名" prop="realname">
                        <el-input v-model.trim="form.realname"  placeholder="真实姓名"></el-input>
                    </el-form-item>

                    <el-form-item label="所属银行" prop="contact">
                        <el-input v-model="form.contact"  placeholder="所属银行" ></el-input>
                    </el-form-item>
    
    
    
                    <el-form-item label="绑定银行卡号" prop="bank_number">
                        <el-input v-model.trim="form.bank_number"  placeholder="绑定银行卡号"></el-input>
                    </el-form-item>


                    <el-form-item label="联系方式" prop="iphone_num">
                        <el-input v-model.trim="form.iphone_num"  placeholder="联系方式"></el-input>
                    </el-form-item>
    
    
                    <el-form-item label="标签" prop="tag_id">
                        <el-select v-model="form.tag_id"  multiple  style="width: 100%" placeholder="选择关联标签">
                            <el-option v-for="item in fromRemoteTags"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    
    
                    <el-form-item label="备注" prop="description">
                        <el-input v-model="form.description"  placeholder="备注"></el-input>
                    </el-form-item>
    
    
                </el-form>
            </FormDrawer>
    
            <!-- 批量搜索 || 批量更新 -->
            <FormDrawer ref="formBatchDrawerRef" :title="drawerBatchTitle" @submit="handleBatchSubmit">
                <el-form :model="batchForm" ref="formBatchRef" :rules="batchRules" label-width="80px">
                    <el-form-item label="字段类型" prop="batchType" v-if="batchModify==0">
                        <el-select v-model="batchForm.batchType"   placeholder="请选择字段" clearable filterable style="width: 100%;">
                            <el-option v-for="(item, index) in batchSearchField"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="字段类型" prop="batchType" v-if="batchModify==1">
                        <el-select v-model="batchForm.batchType"   placeholder="请选择字段" clearable filterable style="width: 100%;">
                            <el-option v-for="(item, index) in batchModifyField"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
    
                    <el-form-item label="打上标签" prop="batchType" v-if="batchModify==1 && batchForm.batchType=='tag_id'" >
                        <el-select v-model="batchForm.tag_id"  multiple placeholder="" clearable filterable style="width: 100%;">
                                <el-option v-for="(item, index)  in fromRemoteTags"
                                    :key="item.id"
                                    :label="item.name"
                                    :value="item.id">
                                </el-option>
                        </el-select>
                    </el-form-item>
    
                    <el-form-item label="数据类型" prop="includeDelete">
                        <el-select v-model="batchForm.includeDelete"   placeholder="请选择数据类型" clearable filterable style="width: 100%;">
                            <el-option v-for="(item, index) in batchSearchType"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
    
                    <el-form-item label="搜索部门" prop="owner_id" v-if="batchModify==0">
                        <el-select v-model="batchForm.owner_id"   placeholder="选择搜索的部门" clearable filterable style="width: 100%">
                            <el-option v-for="(item, index) in groups"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
    
                    
    
                    <el-form-item label="搜索内容" prop="batchContent" v-if="batchModify==0">
                        <el-input v-model="batchForm.batchContent" type="textarea" :rows="20" placeholder="搜索的内容，一行一个"></el-input>
                    </el-form-item>
    
                    
    
    
                    <el-form-item label="更新部门" prop="owner_id"  v-if="batchModify==1">
                        <el-select v-model="batchForm.owner_id"   placeholder="选择更新的部门" clearable filterable style="width: 100%">
                            <el-option v-for="(item, index) in groups"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
    
    
                    <el-form-item label="更新数据" prop="batchContent" v-if="batchModify==1">
                        <el-input v-model="batchForm.batchContent" type="textarea" :rows="20" placeholder="更新的数据，一行一个,空格分割，格式: 会员账号 更新的数据; 例如: vip001 AAAAA ，如果更新标签，只需要填写会员账号"></el-input>
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
                            <p>归属部门: <span style="color: red">*必须*</span></p>
                            <p>渠道号:   <span style="color: red">*必须*</span></p>
                            <p>会员账号: <span style="color: red">*必须*</span></p>
                            <p>游戏ID:   <span style="color: red">*必须*</span></p>
                            <p>真实姓名: <span style="color: red">*必须*</span></p>
                            <p>所属银行: <span style="color: red">*必须*</span></p>
                            <p>银行卡:   <span style="color: red">*必须*</span></p>
                            <p>联系方式: <span style="color: red">可无,更新覆盖</span></p>
                            <p>标签: <span style="color: red">只能一个(可无,更新不覆盖)</span></p>
                            <p>备注: <span style="color: red">可无,更新不覆盖</span></p>
                            <el-divider />
                        </div>
                        <!-- <div class="el-upload__tip"> -->
                            <h3 style="color: green;">EXCEL转化后 JSON 总数据: <span style="color: red">{{ excelDataLength }}</span> 条</h3> 
                        <!-- </div> -->
                        
                    </template>
    
                    
                    
                </el-upload>
    
                <!-- <el-select v-model="importOwner.owner_id"   placeholder="" clearable filterable style="width: 100%">
                    <el-option v-for="(item, index) in groups"
                        :key="item.id"
                        :label="item.name"
                        :value="item.id">
                    </el-option>
                </el-select> -->
                
                <el-button size="small" type="primary" @click="handleImport" style="width: 100%">导入</el-button>
    
            </el-drawer>
    
    
    
        <!-- 批量导入错误提示框 -->
        <el-dialog :title='importTitle'  width="30%" v-model="importModel" :close-on-press-escape="false">
            <span>导入新数据: 
                <span style="color:green; margin: 0 1vh;">{{ successTotal }} </span>条; 
            </span>

            <span>导入更新数据: 
                <span style="color: chocolate; margin: 0 1vh;" >{{ updateTotal  }} </span>条;
            </span>

            <span>导入失败数据: 
                <span style="color: red; font-size: 20px; background-color: black; border-radius: 50%; margin: 0 1vh;">{{ errorTotal  }} </span>条
            </span>
            
            
            <el-divider />


                <div v-for="(item, index) in errorData" :key="index">
                    <p>{{ item }}</p>
                </div>



        </el-dialog>


    
            
            <!-- 条件下载模态框 -->
            <FormDialog :title='DialogTitle'  ref="formDialogRef" @submit="dialogSubmit">
                <el-descriptions
                    title="下载到 EXCEL 条件内容"
                    :column="1"
                    size="small"
                    border
                >
                    <el-descriptions-item label="搜索内容">{{ searchForm.keyword }}</el-descriptions-item>
                    <el-descriptions-item label="所属部门">
                        <span v-for="(item, index) in groups" :key="index">
                                <span v-if="item.id == searchForm.owner_id">{{ item.name }}</span>
                        </span>
                    </el-descriptions-item>
                    <el-descriptions-item label="标签">
                        <span v-for="(item, index) in fromRemoteTags" :key="index">
                                <span v-for="(tag_id, index2) in searchForm.owner_tag_id" :key="index2">
                                    <!-- <el-tag v-if="item.id == tag_id" class="ml-1">{{ item.name }}</el-tag> -->
                                    <el-tag class="ml-1" v-if="item.id == tag_id" :color="item.color" effect="light" style="color: #fff !important;">{{ item.name }}</el-tag>
                                </span>
                        </span>
                    </el-descriptions-item>
    
                    <!-- <el-descriptions-item label="创建者">{{ searchForm.contact_user }}</el-descriptions-item>
                    <el-descriptions-item label="更新者">{{ searchForm.last_name }}</el-descriptions-item>
                    <el-descriptions-item label="创建时间">{{ searchForm.start_end ? searchForm.start_end.join('~') : '' }}</el-descriptions-item>
                    <el-descriptions-item label="更新时间">{{ searchForm.update_start_end ? searchForm.update_start_end.join('~'): '' }}</el-descriptions-item> -->
    
                    <el-descriptions-item label="默认">
                        <el-tag size="small" type="danger">如果以上无数据, 没有条件, 则下载所有,否则下载符合相关条件数据</el-tag>
                    </el-descriptions-item>
                </el-descriptions>
            </FormDialog>
    
        </el-card>
    
    </div>
    
        
    
        
    </template>
    
    
    <script setup>
    import { ref,onMounted,onBeforeUnmount,reactive, computed, watchEffect,onDeactivated } from 'vue'
    import {  Delete, Edit } from '@element-plus/icons-vue'
    import { exportExcel,ImporExceltToJson } from '@/utils/exportExcel'
    import { toast,getCurrentTime,dateFormat } from '@/utils/tools'
    import FormDialog from '@/components/FormDialog.vue'
    
    
    import { 
        getTag,
        getGroup,
        getListMemberProfile,
        createMemberProfile,
        updateMemberProfile,
        deleteMemberProfile,
        batchDeleteMember,
        batchExcelImportMemberProfile,
        getTaskMemberProfile,
        // multideleteMember,
        // multirecoverMember,
        // multiclearMember,
        // multiGetMember,
        // multiModifyMember,
        // multiFromExcelImportMember,
        // countMemberCaiJin
    } from "@/api/memberProfile"
    import ListHeader from '@/components/ListHeader.vue';
    import FormDrawer from '@/components/FormDrawer.vue';
    import { useInitTable,useInitForm } from '@/composables/useCommon'
    import Search from '@/components/Search.vue'
    import SearchItem from '@/components/SearchItem.vue'
    
    
    const groups = ref([])
    const fromRemoteTags = ref([])
    const batchSearchField = ref([])
    const batchModifyField = ref([])
    const batchSearchType = ref([])
    const hiddlePage = ref(true)
    const first_names = ref([])
    const last_names = ref([])
    const users = ref([])
    
    const {
        searchForm,
        resetSearchFrom,
        tableData,
        loading,
        total,
        getData,
        handleDelete,
        handleSelectionChange,
        multipleTableRef,
        handleMultiDelete,
        multiSelectionIds,
        handleRecoverDelete,
        handleClearDelete
    } = useInitTable({
        searchForm: {
            keyword: '',
            skip: 1,
            limit: 10,
            owner_id: null,
            owner_tag_id: [],
            first_name: '',
            last_name: '',
        },
        rules: {
            username: [{
                        required: true,
                        message: '会员账号不能为空',
                        trigger: 'blur',
                    },],
                owner_id: [{
                    required: true,
                    message: '归属部门不能为空',
                    trigger: 'blur',
                },]
        },
    
        onGetListSuccess: (res)=> {
            tableData.value = res.list.map(o=>{
                o.statusLoading = false
                return o
            })
    
    
            total.value = res.totalCount
            users.value = res.users
            // fromRemoteTags.value = res.tags
            // groups.value = res.groups
            // batchSearchField.value = res.batchSearchField
            // batchModifyField.value = res.batchModifyField
            // batchSearchType.value = res.batchSearchType
            hiddlePage.value = true
    
            // console.log(res)
    
        },
        getList: getListMemberProfile,
        delete: deleteMemberProfile,
        multidelete: batchDeleteMember,
        // recoverdelete: multirecoverMember,
        // cleardelete: multiclearMember
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
        handleEdit,
        
        // 返回批量操作内容
        drawerBatchTitle,
        formBatchDrawerRef,
        formBatchRef,
        batchForm,
        batchRules,
        batchModify,
        handleBatchSearch,
        handleBatchModify,
        handleBatchSubmit
    } = useInitForm({
        form: {
            code: '',
            account:'',
            account_id: '',
            realname: '',
            iphone_num: '',
            contact: '',
            bank_number: '',
            description: '',
            owner_id: '',
            tag_id: [],
        },
        rules: {
            code: [{
                required: true,
                message: '渠道号不能为空',
                trigger: 'blur',
            },],
            account: [{
                required: true,
                message: '会员账号不能为空',
                trigger: 'blur',
            },],
            account_id: [{
                required: true,
                message: '游戏ID不能为空',
                trigger: 'blur',
            },],
            realname: [{
                required: true,
                message: '真实姓名不能为空',
                trigger: 'blur',
            },],
            contact: [{
                required: true,
                message: '所属银行不能为空',
                trigger: 'blur',
            },],
            bank_number: [{
                required: true,
                message: '绑定银行卡号不能为空',
                trigger: 'blur',
            },],
            bank_number: [{
                required: true,
                message: '绑定银行卡号不能为空',
                trigger: 'blur',
            },],
            owner_id: [{
                required: true,
                message: '归属部门不能为空',
                trigger: 'blur',
            },],
        },
    
        getData,
        update: updateMemberProfile,
        create: createMemberProfile,
    
        // 批量搜索内容
        batchForm: {
            searchType: '',
            searchContent: '',
            includeDelete: '',
            owner_id: ''
        },
        batchRules: {
            batchType: [
                {
                    required: true,
                    message: '字段类型不能为空',
                    trigger: 'blur',
                },
            ],
            includeDelete: [
                {
                    required: true,
                    message: '数据类型不能为空',
                    trigger: 'blur',
                },
            ],
            batchContent: [
                {
                    required: true,
                    message: '内容不能为空',
                    trigger: 'blur',
                },
            ],
            owner_id: [
                {
                    required: true,
                    message: '搜索部门不能为空',
                    trigger: 'blur',
                },
            ]
        },
        // batchSearch: multiGetMember,
        // batchModify: multiModifyMember,
        onGetBatchSuccess: (res)=> {
            tableData.value = res
            hiddlePage.value = false
        }
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
    
    
    // 分页触发
    const handleCurrentChange = (val) => {
      getData()
    }

    
    
    
    
    
    
    // 导出. ===> 参考: https://juejin.cn/post/7003277929190785061
    // 导出替换某些字段
    
    function fieldReplace(newDate) {
    
    
        console.log(newDate)
        newDate.forEach(e => {
    
            // 部门 ID 替换成部门名称
            groups.value.forEach(b => {
                if(e.owner_id == b.id){
                    e.owner = b.name
                }
            });
    
            // console.log('标签id', e)
    
    
            // 标签 ID  替换成标签名称
            let _tag_id = e.tag_id
            let tags = []
            _tag_id.forEach(t1 => {
                
                fromRemoteTags.value.forEach(t2 => {
                    if(t1 == t2.id){
                        tags.push(t2.name)
                    }
                })
            });
            e.tags = tags.join(',')
        });
    
        return newDate
    }
    
    // 返回下载数据头
    function excelField() {
        let _fds = {
            owner: "归属部门",
            code: "渠道号",
            account: "会员账号",
            account_id: "游戏ID",
            realname: "真实姓名",
            iphone_num: "联系方式",
            contact: "所属银行",
            bank_number: "银行卡",
            tags: "标签",
            description: "备注",
            first_name: "创建人",
            last_name: "修改人",
            created_at: "创建时间",
            updated_at: "更新时间",
        };
        return _fds
    }
    
    
    // 当页下载
    const exportToExcel = (val)=> {
        loading.value = true
        let newDate = fieldReplace(tableData.value)
        const fields = excelField()
        exportExcel(newDate, fields, getCurrentTime() + "_会员信息");
        getData()
        loading.value = false
    }
    
    
    
    // 条件下载
    const formDialogRef = ref(null)
    const DialogTitle = ref(null)
    const conditionToExcel = () => {
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
        getListMemberProfile(searchForm).then(async res => {
            toast('数据已获取，开始转换下载......，数据量大的话，会出现卡顿状态，请耐心等等')
            setTimeout(async ()=> {
                let newDate = await fieldReplace(res.list)
                let fields = excelField()
                await exportExcel(newDate, fields, getCurrentTime() + "_会员资料");
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
    const updateTotal = ref(0)
    const errorTotal = ref(0)
    const errorData = ref([])
    
    const importOwner = reactive({
        owner_id: ''
    })
    
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
        exportExcel([], fields, '会员信息导入模板.xlsx');
    
    }
    
    // 点击上传触发
    const  UploadOnChange =  async (ev) => {
    
        toast('检查EXCEL表头格式....', 'warning')
        try {
            setTimeout(async () => {
                loading.value = true
                let data = await ImporExceltToJson(ev)
                let arr = []                    // 存放替换后端接受的格式
    
    
                
                data.forEach((item) => {
                    if (typeof(item["归属部门"]) === 'undefined'
                    || typeof(item['渠道号']) === 'undefined' || typeof(item['会员账号']) === 'undefined'
                    || typeof(item["游戏ID"]) === 'undefined'   || typeof(item["真实姓名"]) === 'undefined'
                    || typeof(item["所属银行"]) === 'undefined' || typeof(item["银行卡"]) === 'undefined') {
                        loading.value = false
                        upload.value.clearFiles()
                        toast('EXCEL表头格式不正确', 'error')
                        throw new Error('EXCEL表头格式不正确')
                    }
    
                    let _replace = {                     // 替换对象
                        owner: item["归属部门"],
                        code: item["渠道号"],
                        account: item['会员账号'],
                        account_id: item['游戏ID'],
                        realname: item['真实姓名'],
                        iphone_num: item['联系方式'],
                        contact: item['所属银行'],
                        bank_number: item['银行卡'],
                        tags: item["标签"],
                        description: item['备注']
                    }
                    arr.push(_replace);
                });
    
                ImportFromExcelJson.value = arr
                
                // console.log(ImportFromExcelJson.value)
                
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
        batchExcelImportMemberProfile({'importData': ImportFromExcelJson.value})
        .then(res=> {
            task_id.value = res.task_id
            drawer.value = false
            excelDataLength.value = 0      // 清空总数
            ImportFromExcelJson.value = [] // 清空数据
            upload.value.clearFiles()      // 清空上传列表
            getData()
            
            toast('文件导入任务已添加,5秒后开始执行')
            timerLoading.value = setInterval(() => {
                doInterval()   
            }, 3000);
    
        })
        .finally(()=>{
            loading.value = false
        })
    }
    
    
    

onMounted(()=> {
    setTimeout(()=>{
        getGroup().then(res => {
            groups.value = res.groups
        })
    },100)


    setTimeout(()=>{
        getTag().then(res => {
            fromRemoteTags.value = res.tags
        })
    },200)

})



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
    percentageLabel.value = '文件上传任务进度 '
    if(percentageValue.value == 100) {
        setTimeout(()=>{
            percentageValue.value = null
            clearInterval(timerLoading.value)
        },1000)
    }

    
})



// 循环定时器
function doInterval() {
    // percentageValue.value = null
    getTaskMemberProfile({'task_id': task_id.value}).then(res => {
            let num = parseInt(res.task.progress)

            

            if (num === 100) {
                percentageValue.value = null
                task_id.value = ''
                clearInterval(timerLoading.value)
                getData()

                // 并展示出来
                var description =  eval('(' + res.task.description + ')');

                toast(`批量导入:${description.insert_total} 条, 更新：${description.update_total} ,失败: ${description.error_total}`, 'warning' )
                importTitle.value = '导入错误详情'
                importModel.value = true
                successTotal.value = description.insert_total
                updateTotal.value = description.update_total
                errorTotal.value = description.error_total
                errorData.value = description.error

            } 
            percentageValue.value = num
        })
}


onDeactivated(() => {
    clearInterval(timerLoading.value);
    percentageValue.value = null
})



    </script>