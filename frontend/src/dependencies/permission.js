import { router, addRoutes }  from '@/router'
import { getToken } from '@/utils/cookies'
import { toast,showFullLoading,hideFullLoading } from '@/utils/tools'
import store from '@/store'


// 全局前置守卫
let hasGetInfo = false
router.beforeEach(async (to, from, next) => {

    // console.log(to,from, next)

    showFullLoading()

    const token = getToken()
    
    // 没有登录，强制跳转到登录页面
    if(!token && to.path != '/login') {
        toast('请先登录', 'error')
        return next({ path: "/login"})
    }


    // 防止重复登录
    if(token && to.path == '/login'){
        return next({ path: from.path ? from.path: '/'})
    }

    // 如果用户登录了，自动获取用户信息，并存储再 vuex 当中
    let hasNewRoutes = false
    if(token && !hasGetInfo){
        let { menus } = await store.dispatch("getinfo")
        hasGetInfo = true
        hasNewRoutes = addRoutes(menus)
    }


    // 设置页面标题
    let title = (to.meta.title ? to.meta.title : "") + "~牛皮编程后台"
    document.title = title

    
    hasNewRoutes ? next(to.fullPath) : next()

    // next()
  })


router.afterEach((to,from)=> hideFullLoading())