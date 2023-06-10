import { ElNotification, ElMessageBox } from 'element-plus'
import nprogress from "nprogress"



// 消息提示
export function toast(message, type = 'success', dangerouslyUseHTMLString = true, duration = 3000) {
    ElNotification({
        message,
        type,
        dangerouslyUseHTMLString,
        duration
    })

}


// 弹窗消息提示
export function showModal(content="提示内容", type="warning", title=""){
    return ElMessageBox.confirm(
        content, 
        title,
        {
            confirmButtonText: "确认",
            cancelButtonText: "取消",
            type,
        }
    )
}


// 弹出输入框 
export function showPrompt(tip, value = ""){
    return  ElMessageBox.prompt(tip, '', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        inputValue: value
      })
}


// 显示全屏 loading
export function showFullLoading() {
    nprogress.start()
}

// 隐藏全屏 loading
export function hideFullLoading() {
    nprogress.done()
}



// 格式化时间

export function dateFormat(time) {
    var date=new Date(time);
    var year=date.getFullYear();
    /* 在日期格式中，月份是从0开始的，因此要加0
     * 使用三元表达式在小于10的前面加0，以达到格式统一  如 09:11:05
     * */
    var month= date.getMonth()+1<10 ? "0"+(date.getMonth()+1) : date.getMonth()+1;
    var day=date.getDate()<10 ? "0"+date.getDate() : date.getDate();
    var hours=date.getHours()<10 ? "0"+date.getHours() : date.getHours();
    var minutes=date.getMinutes()<10 ? "0"+date.getMinutes() : date.getMinutes();
    var seconds=date.getSeconds()<10 ? "0"+date.getSeconds() : date.getSeconds();
    // 拼接
    return year+"-"+month+"-"+day+" "+hours+":"+minutes+":"+seconds;
}



export function getNextDate(date, day) {
    var dd = new Date(date);
    dd.setDate(dd.getDate() + day)
    var y = dd.getFullYear();
    var m = dd.getMonth() + 1 < 10 ? "0" + (dd.getMonth() + 1) : dd.getMonth() + 1;
    var d = dd.getDate() < 10 ? "0" + dd.getDate() : dd.getDate();
    return y + "-" + m + "-" + d;
}




// 当日日期+时间

export function  getCurrentTime() {
    //获取当前时间并打印
    let yy = new Date().getFullYear();
    let mm = new Date().getMonth()+1;
    let dd = new Date().getDate();
    let hh = new Date().getHours();
    let mf = new Date().getMinutes()<10 ? '0'+new Date().getMinutes() : new Date().getMinutes();
    let ss = new Date().getSeconds()<10 ? '0'+new Date().getSeconds() : new Date().getSeconds();
    return yy+'-'+mm+'-'+dd+' '+hh+':'+mf+':'+ss;
}

