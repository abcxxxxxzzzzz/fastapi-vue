<template>
    <el-card shadow="always" class="border-0">
        
        <ListHeader @create="handleCreate" @refresh="getData" v-permission="['createGroup,POST']"></ListHeader>

        <!-- 表格 -->
        <el-table :data="tableData" style="width: 100%" v-loading="loading" v-permission="['getListGroup,GET']">
            <el-table-column prop="name" label="归属名称"/>
            <el-table-column prop="description" label="归属描述" width="380" />
            <el-table-column  label="状态" width="120" v-permission="['updateStatusGroup,PUT']">
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
                        :icon="Edit"
                        @click="handleEdit(scope.row)"
                        v-permission="['modifyGroup,PUT']"
                    /> 

                    <el-popconfirm
                        title="是否要删除该记录"
                        confirmButtonText="确认"
                        cancelButtonText="取消"
                        confirmButtonType="primary"
                        @confirm="handleDelete(scope.row.id)">
                        <template #reference>
                            <el-button size="small" :icon="Delete" type="danger" v-permission="['deleteGroup,DELETE']"/>
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
                <el-form-item label="归属系列" prop="name">
                    <el-input v-model="form.name"  placeholder="归属系列"></el-input>
                </el-form-item>
                <el-form-item label="归属描述" prop="description">
                    <el-input v-model="form.description" type="textarea" :rows="5" placeholder="归属描述"></el-input>
                </el-form-item>

                <el-form-item label="归属状态" prop="status">
                    <el-switch v-model="form.status" :active-value="1"  :inactive-value="0"></el-switch>
                </el-form-item>
            </el-form>
        </FormDrawer>



    </el-card>


    

    
</template>


<script setup>
import { Delete, Edit } from '@element-plus/icons-vue'


import { 
    getGroupList,
    createGroup,
    updateGroup,
    deleteGroup,
    updateGroupStatus,
} from "@/api/group"
import ListHeader from '@/components/ListHeader.vue';
import FormDrawer from '@/components/FormDrawer.vue';
import { useInitTable,useInitForm } from '@/composables/useCommon'



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
    // rules: {
    // title: [{
    //             required: true,
    //             message: '公告标题不能为空',
    //             trigger: 'blur',
    //         },],
    //     content: [{
    //             required: true,
    //             message: '公告内容不能为空',
    //             trigger: 'blur',
    //         },]
    // },

    getList: getGroupList,
    delete: deleteGroup,
    updateStatus: updateGroupStatus
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
    update: updateGroup,
    create: createGroup
})


const handleSizeChange = (val) => {
  getData()
}
const handleCurrentChange = (val) => {
  getData()
}


</script>