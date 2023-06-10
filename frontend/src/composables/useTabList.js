import { ref } from 'vue'
import { useRoute, onBeforeRouteUpdate } from 'vue-router'
import { useCookies } from '@vueuse/integrations/useCookies'
import { router } from '@/router';

 
export function useTabList() {
    const route = useRoute()
    const cookie = useCookies()
    const activeTab = ref(route.path)
    const tabList = ref([
        {
            title: '后台首页',
            path: '/',
        },
    ])

    // 添加标签导航
    function addTab(tab) {
        let noTab = tabList.value.findIndex(t => t.path == tab.path) == -1
        if (noTab) {
            tabList.value.push(tab)
        }

        cookie.set('tabList', tabList.value)
    }


    // 初始化标签导航列表
    function initTabList() {
        let tbs = cookie.get('tabList')
        if (tbs) {
            tabList.value = tbs
        }
    }
    initTabList()

    // 点击导航或者标签路由之前方法
    onBeforeRouteUpdate((to, from) => {
        activeTab.value = to.path
        addTab({
            title: to.meta.title,
            path: to.path
        })
    })

    // 点击导航或者标签路由之后方法
    const changeTab = (t) => {
        // console.log('点击触发:', t)
        activeTab.value = t
        router.push(t)
    }


    // 移除标签
    const removeTab = (t) => {
        // console.log('移除触发:', t)
        let tabs = tabList.value
        let a = activeTab.value
        if (a == t) {
            tabs.forEach((tab, index) => {
                if (tab.path == t) {
                    const nextTab = tabs[index + 1] || tabs[index - 1]
                    if (nextTab) {
                        a = nextTab.path
                    }
                }
            })
        }
        activeTab.value = a
        tabList.value = tabList.value.filter(tab => tab.path != t)

        cookie.set('tabList', tabList.value)
    }


    // 关闭出发方法
    const handleClose = (c) => {
        if (c == "clearAll") {
            activeTab.value = '/'
            tabList.value = [{
                title: '后台首页',
                path: '/'
            }]
        } else if (c == "clearOther") {
            tabList.value = tabList.value.filter(tab => tab.path == '/' || tab.path == activeTab.value)
        }

        cookie.set("tabList", tabList.value)
    }


    return {
        activeTab,
        tabList,
        changeTab,
        removeTab,
        handleClose
    }
}