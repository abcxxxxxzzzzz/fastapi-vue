import axios from 'axios'
import { getToken,removeToken } from '@/utils/cookies'
import { toast } from '@/utils/tools'
import { useCookies } from '@vueuse/integrations/useCookies'
import { router } from '@/router';


const cookie = useCookies()
const service = axios.create({
    baseURL: '/api',
    timeout: 600000
    // baseURL: 'http://ceshi13.dishait.cn',
    // timeout: 1000,
    // headers: {'X-Custom-Header': 'foobar'}
  });



// 添加请求拦截器
service.interceptors.request.use(function (config) {
  
  // 请求时自动添加 token
  const token = getToken()
  if (token) {
    config.headers['X-Token'] = token
  } 
  return config;
}, function (error) {
  // 对请求错误做些什么
  toast(error.response.data.msg)
  return Promise.reject(error);
});




// 添加响应拦截器
service.interceptors.response.use(function (response) {

  // console.log(response)
  
  // 对响应数据做点什么, 直接获取响应数据当中的 data 数据
  return response.data.data;
}, function (error) {


  if(error.response.status === 401) {
    toast(error.response.data.msg || '请求失败', 'error')
    removeToken()

    cookie.remove('tabList')
    // window.location.reload();
    router.push('/login')
    // setTimeout(()=> window.location.reload(), 500)
  }
  // 对响应错误做点什么, 如果错误直接消息提示
  toast(error.response.data.msg|| '请求失败', 'error')
  return Promise.reject(error);
});


export default service

