import axios  from "@/utils/axios";


// 获取个人信息
export function getinfo() {
    return axios.get("/admin/getinfo")
}

// 修改密码
export function updatepassword(data) {
    return axios.post("/admin/updatepassword",data)
}

// 退出
export function logout() {
    return axios.post("/admin/logout")
}



// 多条件
export function getUserList(query={
    // skip: 1,
    // limit: 1,
    // keyword: "",
}) {

    console.log(query)
    let q = []
    for (const key in query) {
        if (query[key]) {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/users/${r}`)
}


// 修改状态
export function updateUserStatus(id, status ) {
    return axios.put(`/admin/user/${id}/status`,{ status })
}

// 修改密码
export function updateUserPwd(data) {
    return axios.post(`/admin/user/pwd`,data)
}


// 创建
export function createUser(data) {
    return axios.post("/admin/user",data)
}


// 修改
export function updateUser(id, data) {
    return axios.put(`/admin/user/${id}`,data)
}


// 删除
export function deleteUser(id) {
    return axios.delete(`/admin/user/${id}`)
}


