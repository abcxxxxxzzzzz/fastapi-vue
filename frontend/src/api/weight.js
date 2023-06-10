import axios  from "@/utils/axios";



// export function getTagList() {
//     return axios.get("/admin/tags")
// }

export function getWeightList(query={}) {

    console.log(query)
    let q = []
    for (const key in query) {
        if (query[key]  || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/weights/${r}`)
}


export function createWeight(data) {
    return axios.post("/admin/weight",data)
}


export function updateWeight(id,data) {
    return axios.put("/admin/weight/" + id,data)
}


export function deleteWeight(id) {
    return axios.delete(`/admin/weight/${id}`)
}


export function batchCreateWeight(data) {
    return axios.post("/admin/batch/weight", data)
}


// 获取任务进度
export function getTaskCreateWeight(query={}) {
    let q = []
    for (const key in query) {
        if (query[key]) {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    return axios.get(`/admin/batch/weight${r}`)
}



// export function updateTagWebStatus(id,status) {
//     return axios.put(`/admin/weight/${id}/status`,{ status })
// }



export function batchDeleteWeight(ids) {
    ids = !Array.isArray(ids) ? [ids] : ids
    return axios.post("/admin/batch/weight/delete", { ids })
}





// 选中更新
export function batchUpdataWeight(data) {
    return axios.post("/admin/batch/weight/updata", data)
}



// 条件删除
export function ConditionBatchDeleteWeigh(query={}) {

    let q = []
    for (const key in query) {
        if (query[key]  || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.post(`/admin/batch/weight/delete/condition${r}`)
}



// 条件更新
export function ConditionBatchUpdateWeigh(query={}, data) {

    let q = []
    for (const key in query) {
        if (query[key]  || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.post(`/admin/batch/weight/update/condition${r}`, data)
}
