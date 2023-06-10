<template>
    <el-card shadow="always" class="border-0">

        <Search :model="searchForm" @search="getData" @reset="resetSearchFrom">
            <SearchItem label="关键词">
                <el-input v-model="searchForm.keyword" placeholder="搜索关键词" clearable></el-input>
            </SearchItem>
        </Search>

        <!-- 搜索 -->
        <!-- <el-form :model="searchForm"  label-width="80px" class="mb-3" size="small">
            <el-row :gutter="20">
                <el-col :span="8" :offset="0">
                    <el-form-item label="关键词">
                        <el-input v-model="searchForm.keyword" placeholder="管理员昵称" clearable></el-input>
                    </el-form-item>
                </el-col>

                <el-col :span="8" :offset="8">
                    <div  class="flex items-center justify-end">
                        <el-button type="primary" @click="getData" >搜索</el-button>
                        <el-button @click="resetSearchFrom">重置</el-button>
                    </div>
                </el-col>
            </el-row>
        </el-form> -->
        

        <!-- 新增|刷新 -->
        <ListHeader @create="handleCreate" @refresh="getData" v-permission="['createUser,POST']"></ListHeader>

        <!-- 表格 -->
        <el-table :data="tableData" style="width: 100%" v-loading="loading" v-permission="['getListUser,GET']">
            <el-table-column label="管理员" align="center">
                <template  #default="{ row }">
                    <div class="flex items-center">
                        <img src="@/assets/img/gw1L2Z5sPtS8GIl.gif" height="30" width="30" style="border-radius: 50%;" v-if="row.avatar == null || row.avatar ==''" />
                        <el-avatar icon="el-icon-user-solid" :size="40"  :src="row.avatar" v-else></el-avatar>
                        <div class="ml-3">
                            <h6>{{ row.username }}</h6>
                            <!-- <small>ID: {{ row.id }}</small> -->
                        </div>
                    </div>
                </template>
            </el-table-column>

            <el-table-column  label="所属角色" align="center">
                <template  #default="{ row }">
                    <!-- {{ row.role?.name || "-" }} -->

                    <span v-for="(item, index) in row.roles" :key="index"> 
                        <el-tag class="ml-2" type="success" v-if="item.status == 1" >{{ item.name }}</el-tag>
                        <el-tag class="ml-2" type="danger" v-else effect="dark">{{ item.name }}(无效)</el-tag>
                    </span>
                </template>
            </el-table-column>

            <el-table-column  label="所属部门" align="center">
                <template  #default="{ row }">
                    <!-- {{ row.role?.name || "-" }} -->

                    <span v-for="(item, index) in row.groups" :key="index"> 
                        <el-tag class="ml-2" type="success" v-if="item.status == 1" >{{ item.name }}</el-tag>
                        <el-tag class="ml-2" type="danger" v-else effect="dark">{{ item.name }}(无效)</el-tag>
                    </span>
                </template>
            </el-table-column>

            <el-table-column  label="状态" width="120" v-permission="['updateStatusUser,PUT']">
                <template  #default="{ row }">
                    <el-switch 
                        v-model="row.status" 
                        :active-value="1" 
                        :inactive-value="0"
                        :statusLoading = "row.statusLoading"
                        :disabled="row.is_super == 1"
                        @change="handleStatusChange($event,row)">
                    </el-switch>
                    
                </template>
            </el-table-column>


            <el-table-column label="操作">
                <template #default="scope">
                    <small v-if="scope.row.is_super == 1" class="text-sm text-gray-500">暂无操作</small>
                    <div v-else>
                        <el-button 
                            size="small" 
                            :icon="Edit"
                            @click="handleEdit(scope.row)"
                            v-permission="['modifyUser,PUT']"
                        />

                        <el-popconfirm
                            title="是否要删除该公共"
                            confirmButtonText="确认"
                            cancelButtonText="取消"
                            confirmButtonType="primary"
                            @confirm="handleDelete(scope.row.id)">
                            <template #reference>
                                <el-button size="small" :icon="Delete" type="danger" v-permission="['deleteUser,DELETE']"/>
                            </template>
                        </el-popconfirm>
                    </div>
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
                <el-form-item label="用户名" prop="title" placeholder="用户名">
                    <el-input v-model="form.username"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password" placeholder="密码">
                    <el-input v-model="form.password" type="password"></el-input>
                </el-form-item>
                <el-form-item label="头像" prop="avatar">
                    <!-- <ChooseImage v-model="form.avatar"></ChooseImage> -->
                    <el-input v-model="form.avatar" type="text"></el-input>
                </el-form-item>
                <el-form-item label="所属角色" prop="role_id">
                    <el-select v-model="form.role_id"  multiple  style="width: 100%" placeholder="选择所属角色">
                        <el-option v-for="item in roles"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="所属部门" prop="group_id">
                    <el-select v-model="form.group_id"  multiple  style="width: 100%" placeholder="选择所属部门">
                        <el-option v-for="item in groups"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id">
                        </el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="状态" prop="status">
                    <el-switch v-model="form.status" :active-value="1" :inactive-value="0">
                    </el-switch>
                </el-form-item>
                
            </el-form>
            
        </FormDrawer>
    </el-card>


    

    
</template>


<script setup>
import { Delete, Edit } from '@element-plus/icons-vue'
import { ref,onMounted,onBeforeUnmount   } from 'vue'
import ListHeader from '@/components/ListHeader.vue';
import FormDrawer from '@/components/FormDrawer.vue';
import { getUserList,updateUserStatus,createUser,updateUser,deleteUser } from "@/api/user"
import { useInitTable,useInitForm } from '@/composables/useCommon'
import Search from '@/components/Search.vue'
import SearchItem from '@/components/SearchItem.vue'


const roles = ref([])
const groups = ref([])




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
    handleStatusChange
} = useInitTable({
    searchForm: {
        keyword: '',
        skip: 1,
        limit: 10
    },
    getList: getUserList,
    onGetListSuccess: (res)=> {
        tableData.value = res.list.map(o=>{
            o.statusLoading = false
            return o
        })

        
        total.value = res.totalCount
        roles.value = res.roles
        groups.value = res.groups

    },
    delete: deleteUser,
    updateStatus: updateUserStatus
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
        username:'',
        password: '',
        avatar: '',
        role_id: [],
        group_id: [],
        status: 1,
    },
    getData,
    update: updateUser,
    create: createUser
})




// const handleRolesSelect = (val)=> {
//     // console.log(val)
//     let changeFormRoles = []
//     val.forEach(e => {
//         // console.log(typeof e)
//         if (typeof e == 'object') {
//             changeFormRoles.push(e.id)
//         } else {
//             changeFormRoles.push(e)
//         }
        
//     });
//     form.roles = changeFormRoles
// }
// const handleGroupsSelect = (val)=> {
//     // console.log(val)
//     let changeFormRoles = []
//     val.forEach(e => {
//         // console.log(typeof e)
//         if (typeof e == 'object') {
//             changeFormRoles.push(e.id)
//         } else {
//             changeFormRoles.push(e)
//         }
        
//     });
//     form.groups = changeFormRoles
// }



const handleSizeChange = (val) => {
    // console.log(searchForm)
//   console.log(`${val} items per page`)
  getData()
}
const handleCurrentChange = (val) => {
//   console.log(`current page: ${val}`)
  getData()
}




// 监听回车事件
function onKeyUp(e){
    // console.log(e)
    if(e.key == 'Enter') getData();
}

// 添加键盘添加
onMounted(()=>{
    document.addEventListener('keyup', onKeyUp)
})

// 移除键盘监听
onBeforeUnmount(()=>{
    document.removeEventListener('keyup', onKeyUp)
})
</script>