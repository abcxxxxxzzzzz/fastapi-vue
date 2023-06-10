import axios  from "@/utils/axios";



// export function getTagList() {
//     return axios.get("/admin/tags")
// }

export function getTagList(query={}) {

    let q = []
    for (const key in query) {
        if (query[key]) {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/member/tags/list/${r}`)
}


export function createTag(data) {
    return axios.post("/admin/member/tag/create",data)
}


export function updateTag(id,data) {
    return axios.put(`/admin/member/tag/${id}/update`,data)
}


export function deleteTag(id) {
    return axios.delete(`/admin/member/tag/${id}/delete`)
}


