<template>
    <el-card shadow="always" class="border-0">
        <ListHeader @create="handleCreate" @refresh="getData" v-permission="['createPermission,POST']"/>
        <el-tree 
            :data="tableData"  
            :props="{ label: 'name', children: 'children'}" 
            v-loading="loading"
            node-key="id"
            :default-expanded-keys="defaultExpandedKeys	"
            v-permission="['getListPermission,GET']"
        >
            <template #default="{ node, data }">
                <div class="custom-tree-node">
                    <!-- 左 -->
                    <el-tag :type="data.menu ? '': 'info'" size="small">
                        {{ data.menu ? "菜单":"权限" }}
                    </el-tag>
                    <el-icon v-if="data.icon" :size="10" class="ml-2">
                        <component :is="data.icon"></component>
                    </el-icon>
                    <span>&nbsp;&nbsp;{{ data.name }}</span>
                    
                    <!-- 右 -->
                    <div class="ml-auto">
                        <el-switch :modelValue="data.status" :active-value="1" :inactive-value="0" @change="handleStatusChange($event,data)" v-permission="['updateStatusPermission,PUT']"></el-switch>
                        <el-button text type="primary" size="small" :icon="Edit" @click.stop="handleEdit(data)" v-permission="['modifyPermission,PUT']"/>
                        <el-button text type="primary" size="small" :icon="Plus" @click.stop="addChild(data.id)" v-permission="['createPermission,POST']"/>
                        <!-- <el-button text type="primary" size="small">删除</el-button> -->
                        <el-popconfirm
                            title="是否要删除该记录"
                            confirmButtonText="确认"
                            cancelButtonText="取消"
                            confirmButtonType="primary"
                            @confirm="handleDelete(data.id)">
                            <template #reference>
                                <el-button text size="small" :icon="Delete" type="primary" v-permission="['deletePermission,DELETE']"/>
                            </template>
                        </el-popconfirm>
                        
                    </div>

                </div>
            </template>
        </el-tree>



        <!-- 抽屉 -->

        <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit">
            <el-form :model="form" ref="formRef" :rules="rules" label-width="80px">
                <el-form-item label="上级菜单" prop="parent_id">
                    <el-cascader 
                        v-model="form.parent_id"
                        :options="options" 
                        :props="{ value:'id',label: 'name', children: 'children', checkStrictly: true, emitPath:false}"
                        placeholder="请选择上级菜单"
                        >
                    </el-cascader>
                    
                </el-form-item>
                <el-form-item label="菜单/规则" prop="menu">
                    <el-radio-group v-model="form.menu">
                        <el-radio :label="1">菜单</el-radio>
                        <el-radio :label="0">规则</el-radio>
                    </el-radio-group>
                    
                </el-form-item>
                <el-form-item label="名称" prop="name">
                    <el-input v-model="form.name"  style="width: 30%" placeholder="请输入名称"></el-input>
                </el-form-item>
                <el-form-item label="菜单图标" prop="icon" v-if="form.menu == 1">
                    <!-- <el-input v-model="form.icon" ></el-input> -->
                    <IconSelect v-model="form.icon" ></IconSelect>
                </el-form-item>
                <el-form-item label="前端路由" prop="frontpath" v-if="form.menu == 1">
                    <el-input v-model="form.frontpath" placeholder="目录菜单默认不填写"></el-input>
                </el-form-item>
                <el-form-item label="权限标识" prop="code" v-if="form.menu == 0">
                    <el-input v-model="form.code"  placeholder="请输入后端规则"></el-input>
                </el-form-item>
                <el-form-item label="请求方式" prop="method" v-if="form.menu == 0">
                    <el-select v-model="form.method" placeholder="请选择请求方式">
                        <el-option v-for="item in ['GET','POST','PUT','DELETE']"
                            :key="item"
                            :label="item"
                            :value="item">
                        </el-option>
                    </el-select>
                    
                </el-form-item>
                <el-form-item label="排序" prop="sort">
                    <el-input-number v-model="form.sort" :min="0" :max="1000">
                    </el-input-number>
                    
                </el-form-item>

            </el-form>
            
        </FormDrawer>

        
    </el-card>
</template>

<script setup>
import { Delete, Edit, Plus } from '@element-plus/icons-vue'
import { ref } from 'vue'
import { getPermissionList,createPermission,updatePermission,updatePermissionStatus,deletePermission } from '@/api/permission'
import FormDrawer from '@/components/FormDrawer.vue';
import ListHeader from '@/components/ListHeader.vue';
import IconSelect from '@/components/IconSelect.vue';
import { useInitTable,useInitForm } from '@/composables/useCommon'


const defaultExpandedKeys = ref([])
const options = ref([])

const {
    loading,
    tableData,
    getData,
    handleDelete,
    handleStatusChange
} = useInitTable({
    getList: getPermissionList,
    onGetListSuccess:(res)=>{
        options.value = res.list
        tableData.value = res.list
        defaultExpandedKeys.value = res.list.map(o=>o.id)
    },
    delete: deletePermission,
    updateStatus: updatePermissionStatus
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
        parent_id: 0,
        menu: 0,
        name: '',
        code:'',
        method: 'GET',
        status: 1,
        sort: 50,
        icon: '',
        frontpath: ''
    },
    rules: {
        
    },

    getData,
    update: updatePermission,
    create: createPermission
})


// 添加子分类
const addChild = (id)=>{
    handleCreate()
    form.parent_id = id
}

</script>


<style>
.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    font-size: 14px;
    padding-right: 8px;
}

.custom-tree-node__content {
    padding: 20px 0;
}

 
</style>