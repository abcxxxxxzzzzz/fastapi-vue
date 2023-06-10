import axios  from "@/utils/axios";


// 历史数据
export function getBatchSearchKeyWordCount() {
    return axios.get('/admin//batch/count/searchkeywords')
}



// 今日数据
export function getSearchKeyWordCount() {
    return axios.get('/admin/count/searchkeywords')
}


// 获取所有序号
export function getSearchKeyWordGroupByNumber() {
    return axios.get('/admin/searchkeywords/groupby/number')
}


// 获取所有提交用户
export function getSearchKeyWordGroupByUser() {
    return axios.get('/admin/searchkeywords/groupby/user')
}



// 获取所有关键词标签
export function getSearchKeyWordGroupByEn() {
    return axios.get('/admin/searchkeywords/groupby/en')
}



// 获取所有已统计时间
export function getSearchKeyWordGroupByCountAt() {
    return axios.get('/admin/count/searchkeywords/groupby/time')
}




// 测试
export function getSearchKeyWordGroupByCountAtTotal(query={}) {
    let q = []
    for (const key in query) {
        if (query[key] || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    // return axios.get(`/admin/searchkeywords/${r}`)
    return axios.get(`/admin/count/searchkeywords/total/${r}`)
}



export function getSearchKeyWordGroupByCountAtchilds(query={}) {
    let q = []
    for (const key in query) {
        if (query[key] || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""
    return axios.get(`/admin/count/searchkeywords/load/childs/${r}`)
}




export function getSearchKeyWordGroupByCountAtExpandChilds(query={}) {
    let q = []
    for (const key in query) {
        if (query[key] || typeof query[key] == "number") {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""
    return axios.get(`/admin/count/searchkeywords/expand/childs/${r}`)
}