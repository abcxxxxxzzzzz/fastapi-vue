import axios  from "@/utils/axios";


export function getWebSiteList(query={}) {

    let q = []
    for (const key in query) {
        if (query[key]) {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
            
        }
    }
    let r = q.join("&")
    r = r ? ("?" + r) : ""

    
    // 生成 ?xxx=xxx&xx=xx&xxx 或者 空
    return axios.get(`/admin/websites/${r}`)
}


export function createWebSite(data) {
    let newVar = data['child'].split('\n')
    let newChild = []

    // 去除空格
    newVar.forEach(e => {
        if (e !== ''){
            newChild.push(e.replace(/\s/g,""))
        }
    });

    // 去重
    data['child'] = [...new Set(newChild)]
    // data['searchContent'] = newContent.filter(item => item !== '');


    return axios.post("/admin/website",data)
}


export function updateWebSite(id,data) {
    console.log(typeof(data['child']))

    if (typeof data['child'] == "string") {
        let newVar = data['child'].split('\n')
        let newChild = []

        // 去除空格
        newVar.forEach(e => {
            if (e !== ''){
                newChild.push(e.replace(/\s/g,""))
            }
        });

        // 去重
        data['child'] = [...new Set(newChild)]
    }
    return axios.put("/admin/website/" + id,data)
}


export function deleteWebSite(id) {
    return axios.delete(`/admin/website/${id}`)
}

// 批量删
export function multideleteWebSite(ids) {
    ids = !Array.isArray(ids) ? [ids] : ids
    return axios.post("/admin/website/multi", { ids })
}

// 批量还原
export function multirecoverWebSite(ids) {
    ids = !Array.isArray(ids) ? [ids] : ids
    return axios.post("/admin/website/recover", { ids })
}

// 批量彻底删除
export function multiclearWebSite(ids) {
    ids = !Array.isArray(ids) ? [ids] : ids
    return axios.post("/admin/website/clear", { ids })
}

// 批量搜索
export function multiGetWebSite(data) {
    let newVar = data['batchContent'].split('\n')
    let newContent = []

    // 去除空格
    newVar.forEach(e => {
        if (e !== ''){
            newContent.push(e.replace(/\s/g,""))
        }
    });

    // 去重
    data['batchContent'] = [...new Set(newContent)]
    // data['searchContent'] = newContent.filter(item => item !== '');

    return axios.post("/admin/website/search/multi", data)
}


// // 批量更新
export function multiModifyWebSite(data) {

    // if (typeof data['batchContent'] == "string") {
    //     let newVar = data['batchContent'].split('\n')
    //     let a = newVar.filter(item => item !== '')
    //     let b = [...new Set(a)]
        
    //     let newData = []
    //     b.forEach(e => {
    //         let newE = e.split('=>', 2)
    //         // let _aaa = "{\"" + newE[0] + "\":\""  + newE[1] + "\"}"

    //         let _aaa = "{\"code\":\"" + newE[0] + "\",\"value\":\""  + newE[1] + "\"}"
    //         newData.push(JSON.parse(_aaa))
    //     });

        
    //     data['batchContent'] = newData
    // } 

    return axios.post("/admin/website/modify/multi", data)
}



export function multiFromExcelImportWebSite(data) {

    return axios.post(`/admin/website/import`,data)
}


