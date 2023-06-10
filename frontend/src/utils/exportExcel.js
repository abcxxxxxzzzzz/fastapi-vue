import fs from 'file-saver'
import * as XLSX from 'xlsx'

// 导出封装
export function exportExcel(json, fields, filename = '测试数据.xlsx') {
    json.forEach(item => {
        for (let i in item) {
            if (fields.hasOwnProperty(i)) {
                item[fields[i]] = item[i];
            }
            delete item[i]; //删除原先的对象属性
        }
    })
 
    let sheetName = filename //excel的文件名称
    let wb = XLSX.utils.book_new()  //工作簿对象包含一SheetNames数组，以及一个表对象映射表名称到表对象。XLSX.utils.book_new实用函数创建一个新的工作簿对象。
    let ws = XLSX.utils.json_to_sheet(json, { header: Object.values(fields) }) //将JS对象数组转换为工作表。
    wb.SheetNames.push(sheetName)
    wb.Sheets[sheetName] = ws
    const defaultCellStyle = { font: { name: "Verdana", sz: 13, color: "FF00FF88" }, fill: { fgColor: { rgb: "FFFFAA00" } } };//设置表格的样式
    let wopts = { bookType: 'xlsx', bookSST: false, type: 'binary', cellStyles: true, defaultCellStyle: defaultCellStyle, showGridLines: false }  //写入的样式
    let wbout = XLSX.write(wb, wopts)
    let blob = new Blob([s2ab(wbout)], { type: 'application/octet-stream' })
    fs.saveAs(blob, filename + '.xlsx')
}
const s2ab = s => {
    if (typeof ArrayBuffer !== 'undefined') {
        var buf = new ArrayBuffer(s.length)
        var view = new Uint8Array(buf)
        for (var i = 0; i != s.length; ++i) view[i] = s.charCodeAt(i) & 0xff
        return buf
    } else {
        var buf = new Array(s.length);
        for (var i = 0; i != s.length; ++i) buf[i] = s.charCodeAt(i) & 0xFF;
        return buf;
    }
}




const readFile = file => {
    return new Promise((resolve) => {
      let reader = new FileReader();
      reader.readAsBinaryString(file);
      reader.onload = (ev) => {
        resolve(ev.target.result);
      };
    });
  }


export async function  ImporExceltToJson(ev) {

    let file = ev.raw;
    if (!file) return;
    let data = await readFile(file);
    let workbook = XLSX.read(data, { type: "binary" , cellDates: true}),
      worksheet = workbook.Sheets[workbook.SheetNames[0]];

    data = XLSX.utils.sheet_to_json(worksheet);
    // let arr = [];
    // data.forEach((item) => {
    //   arr.push({
    //     username: item["姓名"],
    //     realname: item["VIP"],
    //   });
    // });
    //   //   经转换后
    // console.log("经转换后",arr)
    return data

}



// 导入封装
// export function  ImporExceltToJson(ev) {

//     let file = ev.raw;
//     if (!file) return;

//     let fileReader = new FileReader();
//     fileReader.readAsBinaryString(file);

//     fileReader.onload = (ev)  => {
//         try {
//             const data = ev.target.result
//             const workbook = XLSX.read(data, {
//                 type: 'binary'
//             })
//             const wsname = workbook.SheetNames[0] //取第一张表

//             const ws = XLSX.utils.sheet_to_json(workbook.Sheets[wsname]) //生成json表格内容
            

//             let arr = [];                    // 存放替换后端接受的格式
//             ws.forEach((item) => {
//                 arr.push({
//                     username: item["姓名"],
//                     realname: item["VIP"],
//                 });
//             });

//             console.log('转换的数据',ws)
//             return ws

//         } catch (e) {
//             console.log(e)
//             return false
//         }
//     }
// }
