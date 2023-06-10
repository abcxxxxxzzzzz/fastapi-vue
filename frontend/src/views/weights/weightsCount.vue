<template>
    <el-card shadow="always" class="border-0">
        <Search @model="searchForm" @search="getData" @reset="resetSearchFrom">

                <SearchItem label="已统计时间">
                    <el-select v-model="searchForm.tday" @change="getData"  placeholder="" clearable filterable>
                        <el-option v-for="(item, index) in history"
                            :key="item"
                            :label="item"
                            :value="item">
                        </el-option>
                    </el-select>
                </SearchItem>

        </Search>



<ListHeader :Interval="true"  layout="refresh"  @refresh="getData">
</ListHeader>




        <vxe-table
            border
            :loading="loading"
            :column-config="{resizable: true}"
            :tree-config="{transform: true, rowField: 'time', parentField: 'count_at', lazy: true, hasChild: 'hasChild', loadMethod: loadChildrenMethod}"
            :expand-config="{lazy: true, loadMethod: ExpandChildrenMethod}"
            :data="tableData">
            <vxe-column field="count_at" title="统计日期" tree-node></vxe-column>
            <vxe-column type="expand" width="80">
                <template #content="{ row }">
                    <div class="expand-wrapper" v-if="row.time">
                        <vxe-grid :columns="row.childCols" :data="row.childData" ></vxe-grid>
                    </div>
                </template>
            </vxe-column>
            <vxe-column field="count_total" title="总统计"></vxe-column>
            <vxe-column field="count_sex_total"   title="SEX统计"></vxe-column>
            <vxe-column field="count_other_total" title="OTHER统计"></vxe-column>
            <vxe-column field="count_wrong_total" title="WRONG统计"></vxe-column>
            
        </vxe-table>



                  <!-- 分页 -->
      <vxe-pager
        :layouts="['Sizes', 'PrevJump', 'PrevPage', 'Number', 'NextPage', 'NextJump', 'FullJump', 'Total']"
        :pageSizes="[10, 20, 50, 100]"
        v-model:current-page="searchForm.skip"
        v-model:page-size="searchForm.limit"
        :total="total"
        @page-change="handleCurrentChange">

        <template #right>
            <div class="flex justify-between justify-center">
                <img src="@/assets/img/89fc-fyscsmv5911424.gif" height="20" width="20">
                    <img src="@/assets/img/89fc-fyscsmv5911424.gif" height="20" width="20">
                    <img src="@/assets/img/89fc-fyscsmv5911424.gif" height="20" width="20">
            </div>
            
      </template>
    </vxe-pager>




    </el-card>
</template>

<script setup>
import { ref, reactive } from 'vue'
import Search from '@/components/Search.vue'
import SearchItem from '@/components/SearchItem.vue'
import ListHeader from '@/components/ListHeader.vue';
import { useInitTable,useInitForm } from '@/composables/useCommon'

import { 
getSearchWeightGroupByCountAtTotal,
getSearchWeightGroupByCountAtchilds,
getSearchWeightGroupByCountAtExpandChilds
} from '@/api/weightSearchCount.js'


const tableData = ref([])
const history = ref([])

const { 
searchForm,
loading,
total,
resetSearchFrom,
getData,
} = useInitTable({
searchForm: {
    skip: 1,
    limit: 10,
    tday: '',
    sday: '',
    ssday: '',
    user: '',
},
getList: getSearchWeightGroupByCountAtTotal,
onGetListSuccess:(res)=>{
    tableData.value = res.list
    total.value = res.total
    history.value = res.history
},
})


// 子数据
const loadChildrenMethod = ({ row }) => {

searchForm.sday = row.count_at
// 异步加载子节点
return new Promise(resolve => {
    setTimeout(() => {
        loading.value = true
        let childs = []
        getSearchWeightGroupByCountAtchilds(searchForm).then(res=> {
            childs = res
            resolve(childs)
        }).finally(()=>{
            loading.value = false
        })
            
    }, 200)
})
}

// 子孙数据
const ExpandChildrenMethod = ({ row }) => {
return new Promise((resolve, reject) => {

    if(row.hasChild) {
        console.log('错误',row)
        reject('错误')
    } else {
        setTimeout(() => {
            loading.value = true
            searchForm.ssday = row.time
            searchForm.user = row.count_at
            getSearchWeightGroupByCountAtExpandChilds(searchForm).then(res=> {
                console.log(res)
                row.childCols = res.childCols
                row.childData = res.childData
            }).finally(()=>{
                loading.value = false
            })

            resolve()
        }, 1000)
    }
    
})
}





// 分页触发
const handleCurrentChange = (val) => {
getData()
}

</script>


<style>

.expand-wrapper {
      padding: 20px;
    }
</style>