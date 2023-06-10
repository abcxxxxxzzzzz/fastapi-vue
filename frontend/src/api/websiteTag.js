import axios  from "@/utils/axios";



// export function getTagList() {
//     return axios.get("/admin/tags")
// }

export function getWebTagList(query={}) {

    let q = []
    for (const key in query) {
        if (query[key]) {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/webtags/${r}`)
}


export function createWebTag(data) {
    return axios.post("/admin/webtag",data)
}


export function updateWebTag(id,data) {
    return axios.put("/admin/webtag/" + id,data)
}


export function deleteWebTag(id) {
    return axios.delete(`/admin/webtag/${id}`)
}

export function updateTagWebStatus(id,status) {
    return axios.put(`/admin/webtag/${id}/status`,{ status })
}
