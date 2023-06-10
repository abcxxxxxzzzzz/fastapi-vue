<template>
    <el-card shadow="always" class="border-0">
        
        <ListHeader @create="handleCreate" @refresh="getData" v-permission="['createWebTag,POST']"></ListHeader>

        <!-- 表格 -->
        <el-table :data="tableData" style="width: 100%" v-loading="loading" v-permission="['getListWebTag,GET']">
            <el-table-column prop="name" label="标签名称"/>
            <!-- <el-table-column prop="color" label="标签颜色" width="380" /> -->


            <el-table-column  label="标签颜色" width="380">
                <template  #default="{ row }">
                    <!-- <el-tag :type="row.color" size="small">{{ row.name }}</el-tag> -->
                    <el-tag :color="row.color" size="small"  style="color: #fff !important;">{{ row.name }}</el-tag>
                </template>
            </el-table-column>

            

            <el-table-column label="操作">
                <template #default="scope">

                    <el-button 
                        size="small" 
                        :icon="Edit"
                        @click="handleEdit(scope.row)"
                        v-permission="['modifyWebTag,PUT']"
                    /> 

                    <el-popconfirm
                        title="是否要删除该记录"
                        confirmButtonText="确认"
                        cancelButtonText="取消"
                        confirmButtonType="primary"
                        @confirm="handleDelete(scope.row.id)"
                        >
                        <template #reference v-permission="['deleteWebTag,DELETE']">
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
                <el-form-item label="标签名称" prop="name">
                    <el-input v-model="form.name"  placeholder="标签名称"></el-input>
                </el-form-item>
                <!-- <el-form-item label="标签颜色" prop="color">
                    <el-select v-model="form.color"   style="width: 100%" placeholder="选择所属颜色" >
                        <el-option v-for="item in tags"
                            :key="item.label"
                            :label="item.label"
                            :value="item.value">

                            <el-tag :type="item.value" style="width: 20%;" size="small">{{ item.label }}</el-tag>
                        </el-option>
                    </el-select>
                </el-form-item> -->


                <!-- 自定义颜色 -->
                <el-form-item label="标签颜色" prop="name">
                    <el-color-picker v-model="form.color" show-alpha @change="tagChangeColor"/>
                </el-form-item>

                <!-- <el-form-item label="部门状态" prop="status">
                    <el-switch v-model="form.status" :active-value="1"  :inactive-value="0"></el-switch>
                </el-form-item> -->
            </el-form>
        </FormDrawer>



    </el-card>


    

    
</template>


<script setup>
import { ref } from 'vue'
import { Delete, Edit } from '@element-plus/icons-vue'


import { 
    getWebTagList,
    createWebTag,
    updateWebTag,
    deleteWebTag,
} from "@/api/websiteTag.js"
import ListHeader from '@/components/ListHeader.vue';
import FormDrawer from '@/components/FormDrawer.vue';
import { useInitTable,useInitForm } from '@/composables/useCommon'


const tags = ref([
    {
        'label': 'success',
        'value': 'success',
    },
    {
        'label': 'info',
        'value': 'info',
    },
    {
        'label': 'warning',
        'value': 'warning',
    },
    {
        'label': 'danger',
        'value': 'danger',
    }
])

const {
    searchForm,
    tableData,
    loading,
    // currentPage,
    total,
    // limit,
    getData,
    handleDelete,
    // handleStatusChange
} = useInitTable({
    searchForm: {
        keyword: '',
        skip: 1,
        limit: 10
    },
    rules: {
        name: [{
                    required: true,
                    message: '标签名称不能为空',
                    trigger: 'blur',
                },],
        // color: [{
        //         required: true,
        //         message: '标签颜色不能为空',
        //         trigger: 'blur',
        //     },]
    },

    getList: getWebTagList,
    delete: deleteWebTag,
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
        name:'',
        color: 'rgba(249, 247, 247, 1)',
    },
    rules: {
        name: [{
                required: true,
                message: '标签名称不能为空',
                trigger: 'blur',
            },],
        // color: [{
        //         required: true,
        //         message: '标签颜色不能为空',
        //         trigger: 'blur',
        //     },],
    },

    getData,
    update: updateWebTag,
    create: createWebTag
})


const handleSizeChange = (val) => {
  getData()
}
const handleCurrentChange = (val) => {
  getData()
}



// 自定义颜色
// const tagColor = ref('rgba(19, 206, 102, 0.8)')

const tagChangeColor = (val) => {
    console.log(val)
    form.color = val
}
</script>