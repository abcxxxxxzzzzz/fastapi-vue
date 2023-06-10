import axios  from "@/utils/axios";



// export function getTagList() {
//     return axios.get("/admin/tags")
// }

export function getKeyWordList(query={}) {

    console.log(query)
    let q = []
    for (const key in query) {
        if (query[key] || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/keywords/${r}`)
}




// 获取关键词类别
export function getKeyWordType() {
    return axios.get("/admin/keyword/type")
}



export function createKeyWord(data) {
    return axios.post("/admin/keyword",data)
}


export function updateKeyWord(id,data) {
    return axios.put("/admin/keyword/" + id,data)
}


export function deleteKeyWord(id) {
    return axios.delete(`/admin/keyword/${id}`)
}


export function batchCreateKeyWord(data) {
    return axios.post("/admin/batch/keyword", data)
}

// export function updateTagWebStatus(id,status) {
//     return axios.put(`/admin/keyword/${id}/status`,{ status })
// }



export function batchDeleteKeyWord(ids) {
    ids = !Array.isArray(ids) ? [ids] : ids
    return axios.post("/admin/batch/keyword/delete", { ids })
}



// 选中更新
export function batchUpdataKeyWord(data) {
    return axios.post("/admin/batch/keyword/updata", data)
}




// 条件更新
export function ConditionBatchUpdateKeyword(query={}, data) {

    let q = []
    for (const key in query) {
        if (query[key]  || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.post(`/admin/batch/keyword/update/condition${r}`, data)
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

    return axios.get(`/admin/batch/keyword/download${r}`)
}

