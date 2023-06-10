<template>
    <div>
        <el-tabs v-model="searchForm.tab"  @tab-change="getData" >
            <el-tab-pane :label="item.label" :name="item.name" v-for="(item, index) in tabbars" :key="index"></el-tab-pane>
        </el-tabs>
    
        <el-card shadow="always" class="border-0">
    
            <!-- 搜索 -->
            <Search @model="searchForm" @search="getData" @reset="resetSearchFrom">
                <SearchItem label="关键词">
                    <!-- <el-input v-model="searchForm.keyword" placeholder="全局模糊搜索" @keyup.enter="getData" clearable></el-input> -->

                        <el-input
                            placeholder="默认全局模糊搜索"
                            v-model="searchForm.keyword"
                            @keyup.enter="getData"
                            v-on:input="getData"
                            >
                            <template #prepend>
                                <el-select v-model="searchForm.keywordType"   placeholder="请选择" filterable style="width: 90px">
                                    <el-option v-for="(item, index) in keyWordSearchField"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value"
                                        >
                                    </el-option>
                                </el-select>

                            </template>
                        </el-input>
                    

                </SearchItem>
    
                <!-- 添加到自定义插槽 -->
                <template #show>
                    <SearchItem label="归属系列">
                        <el-select v-model="searchForm.owner_id"   placeholder="" clearable filterable>
                            <el-option v-for="(item, index) in groups"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id">
                            </el-option>
                        </el-select>
                    </SearchItem>
    
                    <SearchItem label="标签">
                        <el-select v-model="searchForm.owner_tag_id"  multiple placeholder="" clearable filterable>
                            <el-option v-for="(item, index)  in fromRemoteTags"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id"
                                >
                                
                            </el-option>
                        </el-select>
                    </SearchItem>
                    
                </template>
            </Search>
    
            <ListHeader layout="refresh"  @refresh="getData"  >
                <el-button type="primary" size="small" @click="handleCreate" v-if="searchForm.tab == 'all'" v-permission="['createWebSite,POST']"><el-icon><Plus /></el-icon> 新增</el-button>
                <el-button type="info" plain size="small" @click="handleBatchSearch"  v-if="searchForm.tab == 'all'" v-permission="['multiSearchWebSite,POST']"><el-icon><Aim /></el-icon> 批量搜索</el-button>
<!--                 
                <el-button type="warning" plain size="small" 
                @click="handleBatchModify"  
                v-if="searchForm.tab == 'all'" 
                > <el-icon><Aim /></el-icon> 批量修改</el-button> -->
    
                <el-popconfirm
                    title="是否要自定义修改"
                    confirmButtonText="确认"
                    cancelButtonText="取消"
                    confirmButtonType="warning"
                    @confirm="handleBatchModify"
                    v-if="searchForm.tab == 'all'">
                    <template #reference>
                        <el-button type="warning" plain size="small" v-permission="['multiModifyWebSite,POST']">自定义修改</el-button>
                    </template>
                </el-popconfirm>


                <el-popconfirm
                    title="是否要批量删除选择的记录,可在回收站恢复"
                    confirmButtonText="确认"
                    cancelButtonText="取消"
                    confirmButtonType="primary"
                    @confirm="handleMultiDelete"
                    v-if="searchForm.tab == 'all'">
                    <template #reference>
                        <el-button type="danger" size="small" v-permission="['multideleteWebSite,POST']"><el-icon><ShoppingCart /></el-icon> 批量删除</el-button>
                    </template>
                </el-popconfirm>
    
    
                <el-button  plain size="small"  @click="openUploadFile"  v-if="searchForm.tab == 'all'" v-permission="['importExcelWebSite,POST']"><el-icon><Upload /></el-icon> 文件上传</el-button>
    
                <el-button type="info" plain size="small" 
                    @click="exportToExcel" v-if="searchForm.tab == 'all'"><el-icon><Download /></el-icon> 下载当页数据</el-button>
    
                <!-- <el-button  plain size="small" 
                    @click="showTableChild"><el-icon><View /></el-icon> 展开子域</el-button> -->
    
                <el-popconfirm
                    title="是否要批量恢复选择已删除的记录？"
                    confirmButtonText="确认"
                    cancelButtonText="取消"
                    confirmButtonType="primary"
                    @confirm="handleRecoverDelete"
                    v-if="searchForm.tab == 'delete'">
                    <template #reference>
                        <el-button type="success" size="small" @click="handleRecoverDelete" v-if="searchForm.tab == 'delete'" v-permission="['multirecoverWebSite,POST']"><el-icon><Refresh /></el-icon> 批量还原</el-button>
                    </template>
                </el-popconfirm>
    
    
                <el-popconfirm
                    title="是否要用永久删除选择的记录？"
                    confirmButtonText="确认"
                    cancelButtonText="取消"
                    confirmButtonType="primary"
                    @confirm="handleClearDelete"
                    v-if="searchForm.tab == 'delete'"
                    >
                    <template #reference>
                        <el-button type="danger" size="small"   v-permission="['multiclearWebSite,POST']"> <el-icon><DeleteFilled /></el-icon> 彻底删除</el-button>
                    </template>
                </el-popconfirm>
    
    
                <!-- <el-button type="danger" size="small" @click="handleClearDelete" v-if="searchForm.tab != 'all'" v-permission="['multiclearMember,POST']">彻底删除</el-button> -->
            </ListHeader>
    
            <!-- 表格 -->
            <el-table ref="multipleTableRef" @selection-change="handleSelectionChange"  
                @cell-mouse-leave="mouseLeave" 
                @sort-change="sortChange"
                header-align="center"  
                :default-expand-all="defaultExpandAll"	
                :data="tableData" 
                style="width: 100%; 
                font-size: 1vh;"    
                v-loading="loading" 
                v-permission="['getListWebSite,GET']" 

                border
            >
                <el-table-column fixed type="selection" width="55"/>
                <el-table-column  label="归属系列" align="center">
                    <template  #default="{ row }">
                        <span>{{ row.owner_id ? row.owner.name: '-' }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="channel_code" width="120" label="渠道号" align="center"  />
                <el-table-column prop="name" label="站点主域名" align="center" width="170" />
                
                
                <el-table-column prop="name" label="子域数" align="center" width="65" >
                    <template  #default="{ row }">
                        <!-- <span @click="handleShowChildDomain(row.child)">{{ row.child ? row.child.split('\n').length : 0 }}</span> -->
                        <el-button size="small" link style="width: 100%; height: 100%;" @click="handleShowChildDomain(row)">{{ row.child ? row.child.split('\n').length : 0 }}</el-button>
                    </template>
                </el-table-column>


                <el-table-column prop="name" label="OP链接" align="center" width="95" >
                    <template  #default="{ row }">
                        <el-button
                            type="success"
                            size="small"
                            round
                            @click="copy(row)"
                        >
                        OP复制  
                        </el-button>
                        <!-- <div  v-if="opId == row.id" >
                            <span>{{ row.op_link }}</span>
                            <el-button  size="small" circle @click="copy(row)" ><el-icon ><CopyDocument /></el-icon></el-button>
                        </div> -->
                    </template>
                </el-table-column>

                <!-- <p m="t-0 b-2">子域: {{ Object.prototype.toString.call(props.row.child)==='[object Array]' }}</p> -->
                <!-- <el-table-column label="子域名" width="65"  type="expand"   align="center">
                    <template #default="props">
                        <div class="childStyle">
                            <p m="t-0 b-2">子域: {{ props.row.child.split('\n') }}</p>
                        </div>
                    </template>
                </el-table-column> -->

                <el-table-column label="站点标签" width="100" align="center">
                    <template  #default="{ row }">
                        <span v-for="(item, index) in row.tags" :key="index" > 
                            <el-tag class="ml-2"  :color="item.color" effect="light" style="color: #fff !important;">{{ item.name }}</el-tag>
                        </span>
                    </template>
                </el-table-column>

                <el-table-column prop="gg_position" label="广告位置" width="170" align="center"/>
                <el-table-column label="广告价格" align="center">
                    <template  #default="{ row }">
                        <span>¥: {{ row.gg_price ? row.gg_price : 0 }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="gg_time" label="广告到期" align="center" width="100" sortable="custom" column-key="gg_time" >
                    <template  #default="{ row }">
                        <span>{{ row.gg_time ? dateFormat(row.gg_time).split(' ')[0] : '' }}</span>
                    </template>
                </el-table-column>

                <el-table-column prop="gg_effect" label="广告效果" align="center" />
                

                <el-table-column prop="contact" label="联系方式" align="center"/>
                <el-table-column prop="wallet_address" label="钱包地址" width="300" align="center"/>

                <el-table-column prop="description" label="备注" width="150" align="center"/>
                <el-table-column prop="first_name" label="创建者" align="center"/>
                <el-table-column prop="last_name" label="更新者" align="center"/>
    
    
                <el-table-column label="操作" fixed="right" width="120" v-if="searchForm.tab != 'delete'" align="center">
                    <template #default="scope">
    
                        <!-- <el-button 
                            size="small" 
                            :icon="Edit"
                            @click="handleEditChild(scope.row)"
                            v-permission="['modifyWebSite,PUT']"
                        />  -->



                        <el-button 
                            size="small" 
                            :icon="Edit"
                            @click="handleEdit(scope.row)"
                            v-permission="['modifyWebSite,PUT']"
                        /> 
    
                        <el-popconfirm
                            title="是否要删除该记录"
                            confirmButtonText="确认"
                            cancelButtonText="取消"
                            confirmButtonType="primary"
                            @confirm="handleDelete(scope.row.id)">
                            <template #reference>
                                <el-button size="small" :icon="Delete" type="danger" v-permission="['deleteWebSite,DELETE']"/>
                            </template>
                        </el-popconfirm>
                    </template>
                </el-table-column>
            </el-table>
            <!-- 分页 -->
            <div class="flex items-center justify-center mt-5">
                    <div v-if="hiddlePage">
                        <el-pagination
                            v-model:current-page="searchForm.skip"
                            v-model:page-size="searchForm.limit"
                            :page-sizes="[10, 50, 100, 200, 500]"
                            small="small"
                            background="background"
                            layout="total, sizes, prev, pager, next, jumper"
                            :total="total"
                            @size-change="handleSizeChange"
                            @current-change="handleCurrentChange"
                        />
                    </div>
            </div>
            
    
            <!-- 新增和修改 -->
            <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit">
                <el-form :model="form" ref="formRef" :rules="rules" label-width="80px">
                    <el-form-item label="站点主域" prop="name">
                        <el-input v-model="form.name"  placeholder="站点主域"></el-input>
                    </el-form-item>

                    <el-form-item label="站点子域" prop="child">
                        <el-input v-model="form.child" type="textarea" :rows="10" placeholder="站点子域" @focus="End($event)" id="textarea_id" style="margin-right: 2px" ></el-input>
                    </el-form-item>

                    <el-form-item label="渠道号" prop="channel_code">
                        <el-input v-model="form.channel_code" placeholder="渠道号"></el-input>
                    </el-form-item>

                    <el-form-item label="OP链接" prop="op_link">
                        <el-input v-model="form.op_link" placeholder="OP链接"></el-input>
                    </el-form-item>
                    
                    <el-form-item label="联系方式" prop="contact"  >
                        <el-input v-model="form.contact"  placeholder="联系方式"></el-input>
                    </el-form-item>
                    <el-form-item label="钱包地址"  prop="wallet_address">
                        <el-input v-model="form.wallet_address"  placeholder="钱包地址"></el-input>
                    </el-form-item>


                    <el-form-item label="广告位置" prop="gg_position"  >
                        <el-input v-model="form.gg_position"  placeholder="广告位置"></el-input>
                    </el-form-item>

                    <el-form-item label="广告价格" prop="gg_price"  >
                        <el-input v-model="form.gg_price"  placeholder="广告价格"></el-input>
                    </el-form-item>

                    <el-form-item label="广告到期" prop="gg_time"  >
                        <el-date-picker
                            v-model="form.gg_time"
                            type="date"
                            placeholder="请选择到期时间"
                            format="YYYY-MM-DD"
                            value-format="YYYY-MM-DD"
                            style="width: 100%"
                            clearable
                        />
                    </el-form-item>

                    <!-- <el-form-item label="广告到期" prop="gg_time"  >
                        <el-input v-model="form.gg_time"  placeholder="广告到期"></el-input>
                    </el-form-item> -->


                    <el-form-item label="广告效果" prop="gg_effect"  >
                        <el-input v-model="form.gg_effect"  placeholder="广告效果"></el-input>
                    </el-form-item>


                    <el-form-item label="备注" prop="description">
                        <el-input v-model="form.description"  placeholder="备注"></el-input>
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
                    <el-form-item label="归属系列" prop="owner_id">
                        <el-select v-model="form.owner_id"  style="width: 100%" placeholder="选择归属系列">
                            <el-option v-for="item in groups"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id">
                            </el-option>
                        </el-select>
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
    
                    <el-form-item label="搜索归属" v-if="batchModify==0">
                        <el-select v-model="batchForm.owner_id"   placeholder="默认搜索所有归属,如果选择，只能选择你权限内的归属系列" clearable filterable style="width: 100%">
                            <el-option v-for="(item, index) in groups"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
    
                    
    
                    <el-form-item label="搜索内容" prop="batchContent" v-if="batchModify==0">
                        <el-input v-model="batchForm.batchContent" type="textarea" :rows="20" placeholder="搜索的内容，一行一个,精准搜索"></el-input>
                    </el-form-item>
    
                    
    
    
                    <el-form-item label="更新部门"  prop="owner_id" v-if="batchModify==1">
                        <el-select v-model="batchForm.owner_id"   placeholder="选择更新的部门" clearable filterable style="width: 100%">
                            <el-option v-for="(item, index) in groups"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
    
    
                    <el-form-item label="更新数据" prop="batchContent" v-if="batchModify==1">
                        <el-input v-model="batchForm.batchContent" type="textarea" :rows="20" placeholder="更新的数据，一行一个,空格分割，格式: 渠道号 更新的数据; 例如: 0000 AAAAA ，如果更新标签，只需要填写渠道号"></el-input>
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
                >
                    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                    <div class="el-upload__text">
                        拖入文件到这里 或者<em> 点击上传</em>
                    </div>
                    <template #tip>
                        <div class="el-upload__tip">
                            xlsx/xls 结尾格式; <button text @click="exportToExcelTemplate" style="color: green">模板下载</button>
                            <el-divider />
                            <h3 style="color: red">注意: 已存在数据会更新,不存在数据添加</h3> 
                            <p>归属系列: <span style="color: red">必须</span></p>
                            <p>渠道号码: <span style="color: red">必须</span></p>
                            <p>渠道主域: <span style="color: red">可无；如果不存在,则已站点子域第一条为主域,如果子域不存在,则为空</span></p>
                            <p>站点子域: <span style="color: red">可无；一格一个 或 一格多行</span></p>
                            <p>标签: <span style="color: red">可无,如果添加只可一个标签</span></p>
                            <p>备注: <span style="color: red">可无</span></p>
                            <el-divider />
                        </div>
                        <div class="el-upload__tip">
<!--                             
                            <span v-if="$store.state.user.is_super">EXCEL两列表头格式: 会员账号(必须)  姓名(必须)  手机号码(可无) 银行账号(可无)  身份证号(可无) </span>
                            <span v-else>EXCEL两列表头格式: 会员账号  姓名</span> -->
                        </div>
                        
                    </template>
    
                </el-upload>
    
                
                <el-button size="small" type="primary" v-loading="loading"  @click="handleImport">导入</el-button>
    
            </el-drawer>


            <!-- 上传 -->
            <el-drawer :title="ChildTitle" v-model="ChildDrawer" >
                
                <!-- <p>{{ childList }}</p> -->

                <div v-for="(item, index) in childList" key="index">
                    <div class="mb-0">
                        <a :href="'http://' + item" target="_blank" rel="external  nofollow">{{ item }}</a>
                        <el-divider />
                    </div>
                </div>
    
            </el-drawer>
    


            <!-- 批量添加子域 -->
        </el-card>
    
    </div>
    
        
    
        
    </template>
    
    
    <script setup>
    import { ref,onMounted,onBeforeUnmount,reactive,nextTick  } from 'vue'
    import {  Delete, Edit } from '@element-plus/icons-vue'
    import { exportExcel,ImporExceltToJson } from '@/utils/exportExcel'
    import { toast,dateFormat } from '@/utils/tools'
    
    
    import { 
        getWebSiteList,
        createWebSite,
        updateWebSite,
        deleteWebSite,
        multideleteWebSite,
        multirecoverWebSite,
        multiclearWebSite,
        multiGetWebSite,
        multiModifyWebSite,
        multiFromExcelImportWebSite
    } from "@/api/website"
    import ListHeader from '@/components/ListHeader.vue';
    import FormDrawer from '@/components/FormDrawer.vue';
    import { useInitTable,useInitForm } from '@/composables/useCommon'
    import Search from '@/components/Search.vue'
    import SearchItem from '@/components/SearchItem.vue'
    import useClipboard from "vue-clipboard3"
    
    
    const groups = ref([])
    const fromRemoteTags = ref([])
    const keyWordSearchField = ref([])
    const batchSearchField = ref([])
    const batchModifyField = ref([])
    const batchSearchType = ref([])
    const hiddlePage = ref(true)
    
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
        handleRecoverDelete,
        handleClearDelete
    } = useInitTable({
        searchForm: {
            keyword: '',
            keywordType: 'all',
            skip: 1,
            limit: 10,
            tab: 'all',
            owner_id: null,
            owner_tag_id: [],
            field: '',
            order_by: '',
        },
        rules: {
            name: [{
                        required: true,
                        message: '标签名称不能为空',
                        trigger: 'blur',
                    },],
            color: [{
                    required: true,
                    message: '标签颜色不能为空',
                    trigger: 'blur',
                },]
        },
    
        onGetListSuccess: (res)=> {
            tableData.value = res.list.map(o=>{
                o.statusLoading = false
                return o
            })

    
            
            total.value = res.totalCount
            fromRemoteTags.value = res.tags
            groups.value = res.groups
            keyWordSearchField.value = res.keyWordSearchField
            batchSearchField.value = res.batchSearchField
            batchModifyField.value = res.batchModifyField
            batchSearchType.value = res.batchSearchType
            hiddlePage.value = true
    
            // console.log(res)
    
        },
        getList: getWebSiteList,
        delete: deleteWebSite,
        multidelete: multideleteWebSite,
        recoverdelete: multirecoverWebSite,
        cleardelete: multiclearWebSite
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
            name:'',
            child:'',
            channel_code: '',
            contact: '',
            wallet_address: '',
            description: '',
            // tags: [],
            owner_id: '',
            tag_id: [],
            gg_position: '',
            gg_price:'',
            gg_time: '',
            gg_effect: '',
            op_link: '',
        },
        rules: {
            channel_code: [{
                    required: true,
                    message: '渠道编号不能为空',
                    trigger: 'blur',
                },],
            owner_id: [{
                    required: true,
                    message: '归属系列不能为空',
                    trigger: 'blur',
                },],
        },
    
        getData,
        update: updateWebSite,
        create: createWebSite,
    
        // 批量搜索内容
        batchForm: {
            searchType: '',
            searchContent: '',
            includeDelete: ''
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
            owner_id: [
                {
                    required: true,
                    message: '归属系列不能为空',
                    trigger: 'blur',
                },
            ],
            batchContent: [
                {
                    required: true,
                    message: '更新内容不能为空',
                    trigger: 'blur',
                },
            ]
        },
        batchSearch: multiGetWebSite,
        batchModify: multiModifyWebSite,
        onGetBatchSuccess: (res)=> {
            tableData.value = res
            hiddlePage.value = false
        }
    })
    
    
    const handleSizeChange = (val) => {
      getData()
    }
    const handleCurrentChange = (val) => {
      getData()
    }
    
    
    // // 监听回车事件
    // function onKeyUp(e){
    //     // console.log(e)
    //     if(e.key == 'Enter') getData();
    // }
    
    // // 添加键盘添加
    // onMounted(()=>{
    //     document.addEventListener('keyup', onKeyUp)
    // })
    
    // // 移除键盘监听
    // onBeforeUnmount(()=>{
    //     document.removeEventListener('keyup', onKeyUp)
    // })
    
    const tabbars = [
        {name: 'all', label: '全部'},
        {name: 'delete', label: '回收站'},
    ]
    
    
    
    
    
    
    
    
    
    
    // 导出. ===> 参考: https://juejin.cn/post/7003277929190785061
    function  getCurrentTime() {
        //获取当前时间并打印
        let yy = new Date().getFullYear();
        let mm = new Date().getMonth()+1;
        let dd = new Date().getDate();
        let hh = new Date().getHours();
        let mf = new Date().getMinutes()<10 ? '0'+new Date().getMinutes() : new Date().getMinutes();
        let ss = new Date().getSeconds()<10 ? '0'+new Date().getSeconds() : new Date().getSeconds();
        return yy+'-'+mm+'-'+dd+' '+hh+':'+mf+':'+ss;
    }
    
    
    // 导出替换某些字段
    
    function fieldReplace(newDate) {
        newDate.forEach(e => {
    
            // 部门 ID 替换成部门名称
            groups.value.forEach(b => {
                if(e.owner_id == b.id){
                    e.owner = b.name
                }
            });
    
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
    
    const exportToExcel = ()=> {
    
        loading.value = true
    
        let newDate = fieldReplace(tableData.value)
        
        let fields = {
            owner: "归属系列",
            channel_code: "渠道号码",
            name: "站点主域",
            child: "站点子域",
            op_link: "OP链接",
            contact: "站点联系方式",
            wallet_address: "钱包地址",
            tags: "站点标签",
            gg_position: "广告位置",
            gg_price: "广告价格",
            gg_effect: "广告效果",
            description: "备注",
            is_del: "是否删除",
            first_name: "创建者",
            last_name: "修改者",
            created_at: "创建时间",
            updated_at: "更新时间",
            delete_at: "删除时间"
        };
    
    
        // let data = JSON.parse(JSON.stringify(this.tableData3));  // 如果直接放置数据不行请加上这句
    
        exportExcel(newDate, fields, getCurrentTime());
        getData()
    
        loading.value = true
    }


    // 导入模板下载
    const exportToExcelTemplate = ()=> {
    
        
        let fields = {
            owner: "归属系列",
            channel_code: "渠道号码",
            name: "站点主域",
            child: "站点子域",
            tags: '标签',
            description: "备注",
            
        };

        exportExcel([], fields, 'websiteTemplate.xlsx');

    }

    
    
    
    // 导入
    const drawer = ref(false)
    const upload = ref(null)
    const ImportFromExcelJson = ref([])
  
    
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
    
    
    const  UploadOnChange = async (ev) => {
    
        loading.value = true
        // importOwner.owner_id = ''
    
        let  data = await ImporExceltToJson(ev)
        let arr = [];                    // 存放替换后端接受的格式
        
        data.forEach((item) => {
            let _replace = {                     // 替换对象
                owner: item["归属系列"],
                channel_code: item["渠道号码"],
                name: item['站点主域'],
                child: item['站点子域'],
                tags: item['标签'],
                description: item['备注']
            }
            arr.push(_replace);
        });
    
        ImportFromExcelJson.value = arr
    
        loading.value = false

        // console.log(ImportFromExcelJson.value)


        // 测试
        let newList = []
        arr.forEach(e => {
            let _a = String(e.child)
            if (typeof e.name == "undefined" && _a != "undefined" && _a.length > 0){
                e.name = _a.split('\n')[0] // 如果主域为空，子域有数据,那么子域第一个域名做为主域
            } else if (typeof e.name == "undefined") {
                e.name = ''
            } 

            if(_a != "undefined" && _a.length > 0) {
                e.child = _a.split('\n')
            } else {
                e.child = []
            }

            newList.push(e)
        });
        console.log(newList)
    }
    
    
    
    
    const handleImport = () =>{
        
        if (ImportFromExcelJson.value.length == 0) return toast('无数据上传','warning')
        loading.value = true
        multiFromExcelImportWebSite({'importData': ImportFromExcelJson.value})
        .then(res=> {``
            toast('批量导入成功')
            drawer.value = false
            upload.value.clearFiles() // 清空上传列表
            getData()
        })
        .finally(()=>{
            loading.value = false
        })
    }
    
    
    
    

    // 展开子域

    const defaultExpandAll = ref(false)
    const showTableChild = () => {
        console.log(defaultExpandAll.value)
        defaultExpandAll.value = !defaultExpandAll.value
        getData()
    } 


    // 点击子域数量，显示子域
    const ChildDrawer = ref(false)
    const childList  = ref([])
    const ChildTitle = ref(null)
    const handleShowChildDomain = (row) => {
        if(!row.child) {
            toast("归属系列：" + row.owner.name + "，渠道号：" + row.channel_code + '，无子域', 'info')
            return false
        }

        ChildDrawer.value = true
        ChildTitle.value = "归属系列：" + row.owner.name + "，渠道号：" + row.channel_code
        childList.value = row.child.split('\n')
    }




    // 点击显示
    const opId = ref(0)
    // const handleShowOP = (row) => {
    //         opId.value = row.id
    // }

    // 移除单元格触发
    const mouseLeave = () => {
        opId.value = 0
    }


    const { toClipboard } = useClipboard();
    const copy = async (row) => {
    try {
        await toClipboard(row.op_link);
        // toast('归属系列:'+ row.owner.name + '\n' +'下的渠道号:'+ row.channel_code + 'OP链接复制成功:');
        toast('<p>归属系列: '+ row.owner.name + '</p>' +'<p>渠道号: '+ row.channel_code + '</p><p style="margin-top: 10px;color: green;">OP链接复制成功</p>');

    } catch (e) {
        toast('复制失败 || OP链接不存在','warning')
        console.error(e);
    }
    };




    const sortChange = ({ column, prop, order }) => {
        // console.log(column)
        // console.log(prop)
        // console.log(order)
        searchForm['field'] = prop
        if(order != null) {
            if(order.includes('desc')){
                searchForm['order_by'] = 'desc'
            } else if (order.includes('asc')) {
                searchForm['order_by'] = 'asc'
            }
        } else {
            searchForm['field'] = ''
            searchForm['order_by'] = ''
        }

        getData()
        
    }




    const End = (e)=>{ 

        // 滚动条自动底部
        nextTick(() => {
            const textarea = document.getElementById('textarea_id');
            textarea.scrollTop = textarea.scrollHeight;
        })
        

        //input获取光标显示在最后
        let obj = e.srcElement;
            obj.focus();
        const len = obj.value.length;
        //光标定位要加上 setTimeOut，不然就会重新光标定位失败
        setTimeout(()=>{
            obj.selectionStart = obj.selectionEnd = len;
        },60)
    }      
    </script>






<style setup>
.childStyle {
    text-align: center;
    
    
}

.el-table .el-table__cell {
    padding: 0 0;
    }



.el-textarea__inner::-webkit-scrollbar-thumb {
    background-color: rgba(168, 168, 168, .4)
}

.el-textarea__inner::-webkit-scrollbar {
    width: 20px;
    height: 8px;
    background-color: white;
}


/* .el-tag {
    color: #fff !important;
} */

/* .el-select .el-select__tags-text {
    color: black;
} */


</style>