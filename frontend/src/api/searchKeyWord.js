import axios  from "@/utils/axios";



// export function getTagList() {
//     return axios.get("/admin/tags")
// }

export function getSearchKeyWordGroupBy() {
    return axios.get('/admin/searchkeywords/groupby')
}

// 列表
export function getSearchKeyWordList(query={}) {

    
    let q = []
    for (const key in query) {
        if (query[key] || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/searchkeywords/${r}`)
}

// 创建
export function createSearchKeyWord(data) {
    return axios.post("/admin/searchkeyword",data)
}

// 更新
export function updateSearchKeyWord(id,data) {
    return axios.put("/admin/searchkeyword/" + id,data)
}

// 删除
export function deleteSearchKeyWord(id) {
    return axios.delete(`/admin/searchkeyword/${id}`)
}

// 查看某一个
export function showSearchKeyWord(id) {
    return axios.get(`/admin/searchkeyword/${id}`)
}


// 锁定状态
export function lockSearchKeyWord(id, is_contact ) {
    return axios.put(`/admin/searchkeyword/${id}/lock`,{ is_contact })
}



// 批量锁定
export function batchDeleteSearchKeyWord(ids) {
    ids = !Array.isArray(ids) ? [ids] : ids
    return axios.post("/admin/batch/searchkeyword/delete", { ids })
}


// 批量删除
export function batchLockSearchKeyWord(ids) {
    ids = !Array.isArray(ids) ? [ids] : ids
    return axios.post("/admin/batch/searchkeyword/lock", { ids })
}


// 搜索
export function searchKeyword(query={}) {
    

    let q = []
    for (const key in query) {
        if (query[key] || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/searchkeywords/search/${r}`)
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

    return axios.get(`/admin/batch/searchkeywords/download${r}`)
}

