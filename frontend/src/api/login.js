import axios  from "@/utils/axios";

export function login(username, password) {
    return axios.post("/admin/login", {
        username,
        password
    })
}


export function getinfo() {
    return axios.get("/admin/getinfo")
}
