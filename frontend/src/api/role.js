import axios  from "@/utils/axios";


// export function getRoleList() {
//     return axios.get("/admin/roles")
// }

export function getRoleList(query={}) {

    let q = []
    for (const key in query) {
        if (query[key]) {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/roles/${r}`)
}


export function createRole(data) {
    return axios.post("/admin/role",data)
}


export function updateRole(id,data) {
    return axios.put("/admin/role/" + id,data)
}


export function deleteRole(id) {
    return axios.delete(`/admin/role/${id}`)
}

export function updateRoleStatus(id,status) {
    return axios.put(`/admin/role/${id}/status`,{ status })
}

export function setRolePermissions(id, permissions) {
    return axios.post(`/admin/role/${id}/bind/permission`,{ permissions })
}

