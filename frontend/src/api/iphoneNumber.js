import axios  from "@/utils/axios";

export function getListIphoneNumber(query={}) {

    let q = []
    for (const key in query) {
        if (query[key]) {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/iphone/number/list${r}`)
}

// 创建
export function createIphoneNumber(data) {
    return axios.post("/admin/iphone/number/create",data)
}



// 更新
export function updateIphoneNumber(id, data) {
    return axios.put(`/admin/iphone/number/${id}/update`,data)
}



// 删除
export function deleteIphoneNumber(id) {
    return axios.delete(`/admin/iphone/number/${id}/delete`)
}





// 查看某一个
export function showIphoneNumber(id) {
    return axios.get(`/admin/iphone/number/${id}/show`)
}



// 批量删除
export function batchDeleteIphoneNumber(ids) {
    ids = !Array.isArray(ids) ? [ids] : ids
    return axios.post("/admin/iphone/number/batch/delete", { ids })
}





export function multiFromExcelImportIphoneNumber(data) {
    return axios.post("/admin/iphone/number/batch/import",data)
}


export function getTaskIphoneNumber() {
    return axios.get("/admin/iphone/number/batch/import")
}


