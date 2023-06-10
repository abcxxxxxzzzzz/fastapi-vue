import { ref, reactive } from 'vue'
import { logout, updateUserPwd } from "@/api/user"
import { showModal, toast } from "@/utils/tools"
import { useRouter } from "vue-router"
import { useStore } from "vuex"



export function userRepassword() {
    const store = useStore()
    const router = useRouter()

    // 修改密码,点击登录验证
    const formDrawerRef = ref(null)
    const formRef = ref(null)

    const form = reactive({
        oldpassword: '',
        password: '',
        repassword: '',

    })

    // 定义验证规则
    const rules = {
        oldpassword: [
            {
                required: true,
                message: '旧密码不能为空',
                trigger: 'blur',
            },
        ],
        password: [
            {
                required: true,
                message: '新密码不能为空',
                trigger: 'blur',
            },
        ],
        repassword: [
            {
                required: true,
                message: '确认密码不能为空',
                trigger: 'blur',
            },
        ]
    }


    const onSubmit = () => {
        formRef.value.validate((valid) => {
            if (!valid) {
                // console.log('error')
                toast('不能为空')
                return false
            }

            // 加载动画
            formDrawerRef.value.showLoading()

            updateUserPwd(form).then(res => {
                toast('修改密码成功，请重新登录')
                store.dispatch('logout')
                router.push('/login')
            }).finally(() => {
                formDrawerRef.value.hideLoading()
            })

        })
    }

    const openRePasswordForm = () => formDrawerRef.value.open()

    return {
        formDrawerRef,
        form,
        rules,
        formRef,
        onSubmit,
        openRePasswordForm
    }

}


export function useLogout() {
    const store = useStore()
    const router = useRouter()
    function handleLogout() {
        showModal("是否要退出登录？").then(res => {
            logout().finally(() => {
                // 退出
                store.dispatch('logout')
                // 跳转回登录页
                router.push('/login')
                // 提示退出登录成功
                toast('退出登录成功')
            })
        })
    }

    return {
        handleLogout
    }
}