import axios  from "@/utils/axios";

export function getListRecordOutMoney(query={}) {

    let q = []
    for (const key in query) {
        if (query[key] || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/recordoutmoney/list${r}`)
}


export function createRecordOutMoney(data) {
    return axios.post("/admin/recordoutmoney/create",data)
}


export function updateRecordOutMoney(id,data) {
    return axios.put(`/admin/recordoutmoney/${id}/update`,data)
}


export function deleteRecordOutMoney(id) {
    return axios.delete(`/admin/recordoutmoney/${id}/delete`)
}


// 二次确认
export function statusRecordOutMoney(data) {
    return axios.post(`/admin/recordoutmoney/${data.id}/status`, { status: data.status} )
}



// 接单
export function receRecordOutMoney(id) {
    return axios.post(`/admin/recordoutmoney/${id}/rece`)
}



// 确认订单
export function doneRecordOutMoney(id, data) {
    return axios.post(`/admin/recordoutmoney/${id}/done`,data)
}


// 修改备注
export function descRecordOutMoney(id, description) {
    return axios.put(`/admin/recordoutmoney/${id}/desc`,{description: description})
}






// 批量删除
export function DeletebatchRecordOutMoney(ids) {
    ids = !Array.isArray(ids) ? [ids] : ids
    return axios.post("/admin/recordoutmoney/batch/delete", { ids })
}



// 复制粘贴上传
export function pasteUploadImage(data) {
    return axios.post("/admin/recordoutmoney/image/upload", data)
}






export const   uploadImageAction = "/api/admin/recordoutmoney/image/upload"




