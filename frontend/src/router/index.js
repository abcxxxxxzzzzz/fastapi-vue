import {
    createRouter,
    createWebHashHistory
} from 'vue-router'


import Login from '@/views/login/index.vue'
import Home from '@/views/home/index.vue'
import NotFound from '@/views/404/index.vue'
import Admin from '@/layouts/admin.vue'
import UsersList from '@/views/system/usersList.vue'
import RolesList from '@/views/system/rolesList.vue'
import GroupsList from '@/views/system/groupsList.vue'
import PermissionsList from '@/views/system/permissionsList.vue'
import MemberTagList from '@/views/member/memberTagList.vue'
import MemberList from '@/views/member/memberList.vue'
import MemberProfileList from '@/views/member/memberProfileList.vue'
import IphoneNumberList from '@/views/member/iphoneNumberList.vue'


import WebSiteList from '@/views/website/webSiteList.vue'
import WebTagList from '@/views/website/webTagList.vue'


import CaijinList from '@/views/member/caijinList.vue'
import caijinTagList from '@/views/member/caijinTagList.vue'

import KeyWordList from '@/views/keyword/keyWordList.vue'
import SearchKeyWordList from '@/views/keyword/searchKeyWordList.vue'
import SearchKeyWordCountList from '@/views/keyword/searchKeyWordCountList.vue'


import WeightsManager from '@/views/weights/weightsManager.vue'
import WeightsSearch from  '@/views/weights/weightsSearch.vue'
import WeightsCount from   '@/views/weights/weightsCount.vue'

import RecordOutMoneyList from "@/views/money/recordOutMoneyList.vue"


import Test from '@/views/test.vue'
// 2.定义一些路由
const routes = [
    { path: "/", name: "admin",component: Admin },
    { path: "/login", component: Login,  meta: {'title': '登录'}},
    { path: "/test", component: Test,  meta: {'title': '测试'}},
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound, meta: {'title': '404'} },
]



// 动态路由，用户匹配菜单动态添加路由
const asyncRoutes = [
    { path:"/", name: "/",component: Home, meta:{ title:"后台首页" }},
    { path: '/admin/users', name: '/admin/users', component: UsersList, meta:{title: '用户列表', keepAlive: true } },    
    { path: '/admin/roles', name: '/admin/roles', component: RolesList, meta:{title: '角色列表', keepAlive: true }  },   
    { path: '/admin/groups', name: '/admin/groups', component: GroupsList, meta:{title: '部门列表', keepAlive: true }  },
    { path: '/admin/permissions', name: '/admin/permissions', component: PermissionsList, meta:{title: '部门列表', keepAlive: true }  },

    // 会员汇总
    { path: '/admin/members/tags', name: '/admin/members/tags', component: MemberTagList, meta:{title: '标签列表', keepAlive: true }  },
    { path: '/admin/members', name: '/admin/members', component: MemberList, meta:{title: '会员列表', keepAlive: true }  },
    { path: '/admin/members/profiles', name: '/admin/members/profiles', component: MemberProfileList, meta:{title: '会员信息', keepAlive: true}  },
    { path: '/admin/caijins', name: '/admin/caijins', component: CaijinList, meta:{title: '彩金管理', keepAlive: true }  },
    { path: '/admin/caijins/tags', name: '/admin/caijins/tags', component: caijinTagList, meta:{title: '彩金来源', keepAlive: true }  },
    { path: '/admin/iphone/numbers', name: '/admin/iphone/numbers', component: IphoneNumberList, meta:{title: '手机号码', keepAlive: true }  },
    
    // 站点汇总
    { path: '/admin/websites', name: '/admin/websites', component: WebSiteList, meta:{title: '站点资料', keepAlive: true}  },
    { path: '/admin/webtags', name: '/admin/webtags', component: WebTagList, meta:{title: '站点标签', keepAlive: true}  },


    // 关键词汇总
    { path: '/admin/keywords', name: '/admin/keywords', component: KeyWordList, meta:{title: '关键词管理', keepAlive: true}  },
    { path: '/admin/searchkeywords', name: '/admin/searchkeywords', component: SearchKeyWordList, meta:{title: '关键词已搜索', keepAlive: true}  },
    { path: '/admin/searchkeywords/count', name: '/admin/searchkeywords/count', component: SearchKeyWordCountList, meta:{title: '关键词统计', keepAlive: false}  },


    // 权重汇总
    { path: '/admin/weights', name: '/admin/weights', component: WeightsManager, meta:{title: '权重管理', keepAlive: true}  },
    { path: '/admin/weights/search', name: '/admin/weights/search', component: WeightsSearch, meta:{title: '权重已搜索', keepAlive: true}  },
    { path: '/admin/weights/count', name: '/admin/weights/count', component: WeightsCount, meta:{title: '权重统计', keepAlive: false}  },


    // 出款管理
    { path: '/admin/out/money', name: '/admin/out/money', component: RecordOutMoneyList, meta:{title: '出款管理', keepAlive: false}  },
]

// 3.创建路由实例并传递 `routes` 配置
export const router = createRouter({
    history: createWebHashHistory(),
    routes
}) 



// 动态添加路由的方法,根据路径配置
export function addRoutes(menus) {
    let hasNewRoutes = false
    // console.log(menus)
    const findAndAddRoutesByMenus = (arr) => {
        arr.forEach(e=>{
            let item = asyncRoutes.find(o=>o.path == e.frontpath)
            if (item && !router.hasRoute(item.path)){
                router.addRoute('admin',item)
                hasNewRoutes = true
            }

            if(e.children && e.children.length > 0) {
                findAndAddRoutesByMenus(e.children)
            }
        });
    }

    findAndAddRoutesByMenus(menus)
    return hasNewRoutes
}
