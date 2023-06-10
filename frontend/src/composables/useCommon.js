import { reactive, ref, computed } from 'vue'
import { toast } from '@/utils/tools'

// 列表、分页、搜索、删除、修改状态
export function useInitTable(opt = {}){
    let searchForm = null
    let resetSearchFrom = null
    if(opt.searchForm){
        searchForm = reactive({ ...opt.searchForm })
        resetSearchFrom = ()=> {
            for (const key in opt.searchForm ) {
                searchForm[key] = opt.searchForm[key];
            }
            getData()
        }
    }
        
    
    // 加载动画
    const tableData = ref([])
    const loading = ref(false)
    

    // 分页
    // const currentPage = ref(1)
    const total = ref(0)
    // const limit = ref(10)
        
    // 获取数据
    function getData(p = null){

        // console.log('先执行')
        if (typeof p == "number"){
            currentPage.value = p
        }

        loading.value = true
        opt.getList(searchForm)
        // opt.getList(currentPage.value,searchForm)
        .then(res=>{
            if(opt.onGetListSuccess && typeof opt.onGetListSuccess == "function"){
                opt.onGetListSuccess(res)
            } else {
                // tableData.value = res.list.map(o=>{
                //     o.statusLoading = false
                //     return o
                // })
                tableData.value = res.list
                total.value = res.totalCount
            }

        }).finally(()=>{
            loading.value = false 
        })
    }

    getData()


    // 删除
    const handleDelete = (id)=> {
        loading.value = true
        opt.delete(id).then(res=>{
            toast('删除成功')
            getData()
        }).finally(()=>{
            loading.value = false
        })
    }

    // 修改状态
    const handleStatusChange = (status, row) =>{
        row.statusLoading = true
        opt.updateStatus(row.id, status)
        .then((res)=>{
            toast('修改状态成功')
            row.status = status
        }).finally(()=>{
            row.statusLoading = false
        })
    }


    // 多选选中ID
    const multiSelectionIds = ref([])
    const handleSelectionChange = (e)=> {
        multiSelectionIds.value = e.map(o=>o.id)
    }

    // 批量删除
    const multipleTableRef = ref(null)
    const handleMultiDelete = ()=> {
        loading.value = true
        // console.log(typeof multiSelectionIds.value)
        opt.multidelete(multiSelectionIds.value)
        .then(res => {
            toast('删除成功')
            // 清空选中
            if(multiSelectionIds.value){
                multiSelectionIds.value = []
                // multipleTableRef.clearCheckboxRow()
                // multipleTableRef.value.clearCheckboxRow()
                // console.log('清空后数据,',multiSelectionIds.value)
                // multipleTableRef.value.clearSelection()
            }
            // getData()
        })
        .finally(()=>{
            loading.value = false
            getData()
        })
    }

    // 批量回收
    const handleRecoverDelete = ()=> {
        loading.value = true
        console.log(typeof multiSelectionIds.value)
        opt.recoverdelete(multiSelectionIds.value)
        .then(res => {
            toast('回收成功')
            // 清空选中
            if(multiSelectionIds.value){
                multiSelectionIds.value = []
                // multipleTableRef.value.clearSelection()
            }
            // getData()
        })
        .finally(()=>{
            loading.value = false
            getData()
        })
    }

    // 批量清空回收站
    const handleClearDelete = ()=> {
        loading.value = true
        console.log(typeof multiSelectionIds.value)
        opt.cleardelete(multiSelectionIds.value)
        .then(res => {
            toast('彻底删除成功')
            // 清空选中
            if(multiSelectionIds.value){
                multiSelectionIds.value = []
                console.log('清空后数据,',multiSelectionIds.value)
                // multipleTableRef.value.clearSelection()
            }
            // getData()
        })
        .finally(()=>{
            loading.value = false
            getData()
        })
    }

    return {
        searchForm,
        resetSearchFrom,
        tableData,
        loading,
        // currentPage,
        total,
        // limit,
        getData,
        handleDelete,
        handleStatusChange,
        handleSelectionChange,
        multipleTableRef,
        handleMultiDelete,
        handleRecoverDelete,
        handleClearDelete,
        multiSelectionIds
    }

    
}


//新增，修改
export function useInitForm(opt = {}){
    // 表单部分
    const formDrawerRef = ref(null)
    const formRef = ref(null)
    const defaultForm = opt.form
    const form = reactive({})
    const rules = opt.rules || {}
    const editId = ref(0)
    const drawerTitle = computed(()=> editId.value ? "修改" : "新增")

    const handleSubmit = () => {
        formRef.value.validate((valid)=>{
            if(!valid) return 
    
            formDrawerRef.value.showLoading()
    
            const fun = editId.value ? opt.update(editId.value, form) : opt.create(form)
    
            fun.then(res=>{
                toast(drawerTitle.value + '成功')
    
                // 修改刷新当前页，添加刷新第一页
                // opt.getData(editId.value ? false: 1)
                opt.getData()
                formDrawerRef.value.close()
            }).finally(()=>{
                formDrawerRef.value.hideLoading()
            })
    
        })
    }
    

    // 重置表单
    function resetForm(row=false){
        if(formRef.value) formRef.value.clearValidate()
        if(row){
            for(const key in defaultForm){
                form[key] = row[key]
            }
        }
    }

    // 新增
    const handleCreate = ()=>{
        editId.value = 0
        resetForm(defaultForm)
        formDrawerRef.value.open()
    }


    // 编辑
    const handleEdit = (row)=> {
        editId.value = row.id
        resetForm(row)
        formDrawerRef.value.open()
    }



    // 批量搜索
    const defaultBatchForm = opt.batchform 
    const batchForm = reactive({})
    const formBatchRef = ref(null)
    const formBatchDrawerRef = ref(null)
    const batchRules = opt.batchRules || {}
    const batchModify = ref(0)
    const drawerBatchTitle = computed(()=> batchModify.value ? "自定义修改" : "批量搜索")

    function resetBatchForm(row=false){
        if(formBatchRef.value) formBatchRef.value.resetFields()
        if(row){
            for(const key in defaultBatchForm){
                batchForm[key] = row[key]
            }
        }
    }

    // 触发批量搜索
    const handleBatchSearch = ()=>{
        batchModify.value = 0
        resetBatchForm(defaultBatchForm)
        formBatchDrawerRef.value.open()
    }

    // 触发批量修改
    const handleBatchModify = (row=null)=> {
        batchModify.value = 1
        resetBatchForm()
        formBatchDrawerRef.value.open()
    }


    // 触发提交修改或者搜索
    const handleBatchSubmit = () => {
        formBatchRef.value.validate((valid)=>{
            if(!valid) return 
            formBatchDrawerRef.value.showLoading()

            // opt.batch(batchForm)
            const fun = batchModify.value ? opt.batchModify(batchForm) : opt.batchSearch(batchForm)

            fun.then(res=>{
                if(opt.onGetBatchSuccess && typeof opt.onGetBatchSuccess == "function"){
                    opt.onGetBatchSuccess(res)
                } 

                if (batchModify.value) {
                    opt.getData()
                }
                
                toast(drawerBatchTitle.value + '成功')
                formBatchDrawerRef.value.close()
                
            }).finally(()=>{
                formBatchDrawerRef.value.hideLoading()
            })
        })
    } 




    // 批量添加
        
    return {
        formDrawerRef,
        formRef,
        form,
        rules,
        editId,
        drawerTitle,
        handleSubmit,
        resetForm,
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
    }
}
