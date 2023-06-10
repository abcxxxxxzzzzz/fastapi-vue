import axios  from "@/utils/axios";


export function getMemberList(query={}) {

    let q = []
    for (const key in query) {
        if (query[key]) {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/members/${r}`)
}


export function createMember(data) {
    return axios.post("/admin/member",data)
}


export function updateMember(id,data) {
    return axios.put("/admin/member/" + id,data)
}


export function deleteMember(id) {
    return axios.delete(`/admin/member/${id}`)
}

// 批量删
export function multideleteMember(ids) {
    ids = !Array.isArray(ids) ? [ids] : ids
    return axios.post("/admin/member/multi", { ids })
}

// 批量还原
export function multirecoverMember(ids) {
    ids = !Array.isArray(ids) ? [ids] : ids
    return axios.post("/admin/member/recover", { ids })
}

// 批量彻底删除
export function multiclearMember(ids) {
    ids = !Array.isArray(ids) ? [ids] : ids
    return axios.post("/admin/member/clear", { ids })
}

// 批量搜索
export function multiGetMember(data) {
    let newVar = data['batchContent'].split('\n')
    let newContent = []

    // 去除空格
    newVar.forEach(e => {
        if (e !== ''){
            newContent.push(e.replace(/\s/g,""))
        }
    });

    // 去重
    data['batchContent'] = [...new Set(newContent)]
    // data['searchContent'] = newContent.filter(item => item !== '');

    return axios.post("/admin/member/search/multi", data)
}


// 批量更新
export function multiModifyMember(data) {
    // let newVar = data['batchContent'].split('\n')
    // let a = newVar.filter(item => item !== '')
    // let b = [...new Set(a)]
    
    // let newData = []
    // b.forEach(e => {
    //     let newE = e.split('=>', 2)
    //     // let _aaa = "{\"" + newE[0] + "\":\""  + newE[1] + "\"}"

    //     let _aaa = "{\"vip\":\"" + newE[0] + "\",\"value\":\""  + newE[1] + "\"}"
    //     newData.push(JSON.parse(_aaa))
    // });

    
    // data['batchContent'] = newData


    return axios.post("/admin/member/modify/multi", data)
}

// export function updateMemberStatus(id,status) {
//     return axios.put(`/admin/member/${id}/status`,{ status })
// }





export function multiFromExcelImportMember(data) {
    return axios.post("/admin/member/batch/import",data)
}




// 获取任务进度
export function getTaskMember(query={}) {
    let q = []
    for (const key in query) {
        if (query[key]) {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    return axios.get(`/admin/member/batch/import${r}`)
}




// 计算数值
export function countMemberCaiJin(id) {
    return axios.post(`/admin/member/${id}/caijin`)
}
