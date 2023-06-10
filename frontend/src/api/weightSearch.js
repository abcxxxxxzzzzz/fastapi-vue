import axios  from "@/utils/axios";



// export function getTagList() {
//     return axios.get("/admin/tags")
// }

export function getSearchWeightGroupBy() {
    return axios.get('/admin/searchweights/groupby')
}


export function getSearchWeightList(query={}) {

    
    let q = []
    for (const key in query) {
        if (query[key] || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/searchweights/${r}`)
}


export function createSearchWeight(data) {
    return axios.post("/admin/searchweight",data)
}


export function updateSearchWeight(id,data) {
    return axios.put("/admin/searchweight/" + id,data)
}


export function deleteSearchWeight(id) {
    return axios.delete(`/admin/searchweight/${id}`)
}



// 锁定状态
export function lockSearchWeight(id, is_contact ) {
    return axios.put(`/admin/searchweight/${id}/lock`,{ is_contact })
}




export function batchDeleteSearchWeight(ids) {
    ids = !Array.isArray(ids) ? [ids] : ids
    return axios.post("/admin/batch/searchweight/delete", { ids })
}


export function batchLockSearchWeight(ids) {
    ids = !Array.isArray(ids) ? [ids] : ids
    return axios.post("/admin/batch/searchweight/lock", { ids })
}


// export function updateTagWebStatus(id,status) {
//     return axios.put(`/admin/searchweight/${id}/status`,{ status })
// }


// 获取所有序号
export function getSearchWeightGroupByNumber() {
    return axios.get('/admin/searchweights/groupby/number')
}


// 获取所有提交用户
export function getSearchWeightGroupByUser() {
    return axios.get('/admin/searchweights/groupby/user')
}



// 获取所有关键词标签
export function getSearchWeightGroupByEn() {
    return axios.get('/admin/searchweights/groupby/en')
}




// 查看某一个
export function showSearchWeight(id) {
    return axios.get(`/admin/searchweight/${id}`)
}


// 搜索
export function searchWeight(query={}) {
    

    let q = []
    for (const key in query) {
        if (query[key] || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/searchweights/search/${r}`)
}





// 获取任务进度
export function getTaskProgress(query={}) {
    let q = []
    for (const key in query) {
        if (query[key]) {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    return axios.get(`/admin/batch/searchweights/download${r}`)
}

