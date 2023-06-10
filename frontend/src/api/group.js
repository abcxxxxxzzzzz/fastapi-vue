import axios  from "@/utils/axios";



// export function getGroupList() {
//     return axios.get("/admin/groups")
// }

export function getGroupList(query={}) {

    let q = []
    for (const key in query) {
        if (query[key]) {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/groups/${r}`)
}


export function createGroup(data) {
    return axios.post("/admin/group",data)
}


export function updateGroup(id,data) {
    return axios.put("/admin/group/" + id,data)
}


export function deleteGroup(id) {
    return axios.delete(`/admin/group/${id}`)
}

export function updateGroupStatus(id,status) {
    return axios.put(`/admin/group/${id}/status`,{ status })
}
