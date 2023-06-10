import axios  from "@/utils/axios";



export function getPermissionList() {
    return axios.get("/admin/permissions")
}



export function createPermission(data) {
    return axios.post("/admin/permission",data)
}


export function updatePermission(id,data) {
    return axios.put("/admin/permission/" + id,data)
}


export function updatePermissionStatus(id,status) {
    return axios.put(`/admin/permission/${id}/status`,{ status })
}


export function deletePermission(id) {
    return axios.delete(`/admin/permission/${id}`)
}
