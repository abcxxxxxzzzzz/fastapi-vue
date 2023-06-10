<template>
    <el-card shadow="always" class="border-0">
        
        <ListHeader @create="handleCreate" @refresh="getData" v-permission="['createRole,POST']"></ListHeader>

        <!-- 表格 -->
        <el-table :data="tableData" style="width: 100%" v-loading="loading" v-permission="['getListRole,GET']">
            <el-table-column prop="name" label="角色名称"/>
            <el-table-column prop="description" label="角色描述" width="380" />
            <el-table-column  label="状态" width="120" v-permission="['updateStatusRole,PUT']">
                <template  #default="{ row }">
                    <el-switch 
                        v-model="row.status" 
                        :active-value="1" 
                        :inactive-value="0"
                        :statusLoading = "row.statusLoading"
                        @change="handleStatusChange($event,row)">
                    </el-switch>
                    
                </template>
            </el-table-column>

            <el-table-column label="操作">
                <template #default="scope">
                    <el-button 
                        size="small" 
                        :icon="Monitor"
                        @click="openSetPermission(scope.row)"
                        v-permission="['modifyRole,PUT']"
                    /> 

                    <el-button 
                        size="small" 
                        :icon="Edit"
                        @click="handleEdit(scope.row)"
                        v-permission="['modifyRole,PUT']"
                    />

                    <el-popconfirm
                        title="是否要删除该记录"
                        confirmButtonText="确认"
                        cancelButtonText="取消"
                        confirmButtonType="primary"
                        @confirm="handleDelete(scope.row.id)">
                        <template #reference>
                            <el-button size="small" :icon="Delete" type="danger" v-permission="['deleteRole,DELETE']"/>
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
                <el-form-item label="角色名称" prop="name">
                    <el-input v-model="form.name"  placeholder="角色名称"></el-input>
                </el-form-item>
                <el-form-item label="角色描述" prop="description">
                    <el-input v-model="form.description" type="textarea" :rows="5" placeholder="角色描述"></el-input>
                </el-form-item>

                <el-form-item label="角色状态" prop="status">
                    <el-switch v-model="form.status" :active-value="1"  :inactive-value="0"></el-switch>
                </el-form-item>
            </el-form>
        </FormDrawer>


        <!-- 权限配置 -->
        <FormDrawer ref="setPermissionformDrawerRef" title="权限配置" @submit="handlePermissionSubmit">
            <el-tree-v2  
                ref="elTreeRef"
                :data="permissionList" 
                node-key="id"
                :default-expanded-keys = "defaultExpandedKeys"
                :check-strictly	= "checkStrictly"
                :props="{ label: 'name', children: 'children'}" 
                show-checkbox
                :height="treeHeight" 
                @check="handleTreeCheck"
            >

            <template #default="{ node,data }">
                <div class="flex items-center">
                    <el-tag :type="data.menu ? '': 'info'" size="small">
                        {{ data.menu ? "菜单": "权限" }}
                    </el-tag>
                    <span class="ml-2 text-sm">{{ data.name }}</span>
                </div>
            </template>
            
            
            
            </el-tree-v2>
                
        </FormDrawer>
    </el-card>


    

    
</template>


<script setup>
import { Delete, Edit,Monitor } from '@element-plus/icons-vue'
import { ref } from 'vue'
import { 
    getRoleList,
    createRole,
    updateRole,
    deleteRole,
    updateRoleStatus,
    setRolePermissions 
} from "@/api/role"
import ListHeader from '@/components/ListHeader.vue';
import FormDrawer from '@/components/FormDrawer.vue';
import { useInitTable,useInitForm } from '@/composables/useCommon'
import { getPermissionList } from '@/api/permission'
import { toast } from '@/utils/tools'


const {
    searchForm,
    tableData,
    loading,
    // currentPage,
    total,
    // limit,
    getData,
    handleDelete,
    handleStatusChange
} = useInitTable({
    searchForm: {
        keyword: '',
        skip: 1,
        limit: 10
    },
    rules: {
    title: [{
                required: true,
                message: '公告标题不能为空',
                trigger: 'blur',
            },],
        content: [{
                required: true,
                message: '公告内容不能为空',
                trigger: 'blur',
            },]
    },

    getList: getRoleList,
    delete: deleteRole,
    updateStatus: updateRoleStatus
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
        description: '',
        status: 1,
    },
    rules: {
        name: [{
                required: true,
                message: '角色名称不能为空',
                trigger: 'blur',
            },],
    },

    getData,
    update: updateRole,
    create: createRole
})


const setPermissionformDrawerRef = ref(null)
const permissionList = ref([])
const treeHeight = ref(0)
const permissionId = ref(0)
const defaultExpandedKeys = ref([])
const elTreeRef = ref(null)

//当前角色拥有的权限ID
const permissionIds = ref([])
const checkStrictly = ref(false)

const openSetPermission = (row) => {
    console.log('打开的ID:',row.id)
    permissionId.value = row.id
    treeHeight.value = window.innerHeight - 180
    checkStrictly.value = true
    getPermissionList().then(res=>{
        permissionList.value = res.list
        defaultExpandedKeys.value = res.list.map(o=>o.id)
        setPermissionformDrawerRef.value.open()

        // 当前角色拥有的权限ID
        console.log('当前角色:', row)
        permissionIds.value = row.permissions.map(o=>o.id)
        setTimeout(()=>{
            elTreeRef.value.setCheckedKeys(permissionIds.value)
            checkStrictly.value = false
        },150)

    })
    
}

const handlePermissionSubmit = () => {
    setPermissionformDrawerRef.value.showLoading()
    setRolePermissions(permissionId.value, permissionIds.value).then(res=>{
        toast('配置成功')
        getData()
        setPermissionformDrawerRef.value.close()
    }).finally(()=>{
        setPermissionformDrawerRef.value.hideLoading()
    })
}


const handleTreeCheck = (...e) => {
    const { checkedKeys,halfCheckedKeys } = e[1]
    permissionIds.value = [...checkedKeys, ...halfCheckedKeys]
    console.log(permissionIds.value)
}
// 
const handleSizeChange = (val) => {
  getData()
}
const handleCurrentChange = (val) => {
  getData()
}

</script>