import axios  from "@/utils/axios";


export function getSearchWeightGroupByCountAtTotal(query={}) {
    let q = []
    for (const key in query) {
        if (query[key] || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    // return axios.get(`/admin/searchweights/${r}`)
    return axios.get(`/admin/count/searchweights/total/${r}`)
}



export function getSearchWeightGroupByCountAtchilds(query={}) {
    let q = []
    for (const key in query) {
        if (query[key] || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""
    return axios.get(`/admin/count/searchweights/load/childs/${r}`)
}




export function getSearchWeightGroupByCountAtExpandChilds(query={}) {
    let q = []
    for (const key in query) {
        if (query[key] || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""
    return axios.get(`/admin/count/searchweights/expand/childs/${r}`)
}