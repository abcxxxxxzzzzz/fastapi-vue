import axios  from "@/utils/axios";



// export function getTagList() {
//     return axios.get("/admin/tags")
// }

export function getMemberCaiJinSourceList(query={}) {

    let q = []
    for (const key in query) {
        if (query[key] || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/member/caijin/source/list/${r}`)
}


export function createMemberCaiJinSource(data) {
    return axios.post("/admin/member/caijin/source/create",data)
}


export function updateMemberCaiJinSource(id,data) {
    return axios.put(`/admin/member/caijin/source/${id}/update`, data)
}


export function deleteMemberCaiJinSource(id) {
    return axios.delete(`/admin/member/caijin/source/${id}/delete`)
}

