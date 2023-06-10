import axios  from "@/utils/axios";


export function getTag() {
    return axios.get('/admin/member/profile/tags')
}

export function getGroup() {
    return axios.get('/admin/member/profile/groups')
}


export function getListMemberProfile(query={}) {

    let q = []
    for (const key in query) {
        if (query[key]) {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/member/profile/list/${r}`)
}


export function createMemberProfile(data) {
    return axios.post("/admin/member/profile/create",data)
}


export function updateMemberProfile(id,data) {
    return axios.put(`/admin/member/profile/${id}/update`, data)
}


export function deleteMemberProfile(id) {
    return axios.delete(`/admin/member/profile/${id}/delete`)
}

// 批量删
export function batchDeleteMember(ids) {
    ids = !Array.isArray(ids) ? [ids] : ids
    return axios.post("/admin/member/profile/batch/delete", { ids })
}




// 文件上传
export function batchExcelImportMemberProfile(data) {
    return axios.post("/admin/member/profile/batch/import",data)
}



// 获取任务进度
export function getTaskMemberProfile(query={}) {
    let q = []
    for (const key in query) {
        if (query[key]) {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    return axios.get(`/admin/member/profile/batch/import${r}`)
}



// // 批量搜索
// export function multiGetMember(data) {
//     let newVar = data['batchContent'].split('\n')
//     let newContent = []

//     // 去除空格
//     newVar.forEach(e => {
//         if (e !== ''){
//             newContent.push(e.replace(/\s/g,""))
//         }
//     });

//     // 去重
//     data['batchContent'] = [...new Set(newContent)]
//     // data['searchContent'] = newContent.filter(item => item !== '');

//     return axios.post("/admin/member/search/multi", data)
// }


// // 批量更新
// export function multiModifyMember(data) {
//     return axios.post("/admin/member/modify/multi", data)
// }




// export function multiFromExcelImportMember(data) {
//     return axios.post("/admin/member/import/batch",data)
// }
