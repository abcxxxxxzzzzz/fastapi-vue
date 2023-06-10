import axios  from "@/utils/axios";



export function getStatistics() {
    return axios.get("/admin/getStatistics")
}
