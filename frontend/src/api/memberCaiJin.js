import axios  from "@/utils/axios";


// 搜索单个字符
export function getMemberCaiJinOne(query={}) {
    

    let q = []
    for (const key in query) {
        if (query[key] || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/member/caijin/search/${r}`)
}




export function getMemberCaiJinList(query={}) {

    let q = []
    for (const key in query) {
        if (query[key]) {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/member/caijin/list${r}`)
}

// 创建
export function createMemberCaiJin(data) {
    return axios.post("/admin/member/caijin/create",data)
}



// 更新
export function updateMemberCaiJin(id, data) {
    return axios.put(`/admin/member/caijin/${id}/update`,data)
}



// 删除
export function deleteMemberCaiJin(id) {
    return axios.delete(`/admin/member/caijin/${id}/delete`)
}





// 查看某一个
export function showMemberCaiJin(id) {
    return axios.get(`/admin/member/caijin/${id}/show`)
}



// 批量删除
export function batchDeleteMemberCaiJin(ids) {
    ids = !Array.isArray(ids) ? [ids] : ids
    return axios.post("/admin/member/caijie/batch/delete", { ids })
}





export function multiFromExcelImportMemberCaiJin(data) {
    return axios.post("/admin/member/caijie/batch/import",data)
}




// 获取任务进度
export function getTaskMemberCaiJin(query={}) {
    let q = []
    for (const key in query) {
        if (query[key]) {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    return axios.get(`/admin/member/caijie/batch/import${r}`)
}



// export const   getTaskMemberCaiJin = (task_id) => {
//     return 'ws://' + window.location.host + '/api/admin/ws/member/caijie/batch/import/' + task_id
// }

