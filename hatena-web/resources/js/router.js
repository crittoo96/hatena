import Vue from 'vue'
import VueRouter from 'vue-router'

import UserList
    from "./pages/UserList"
Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        component: UserList
    }
]

// VueRouterインスタンスを作成する
const router = new VueRouter({
    mode: 'history', // ★ 追加
    routes
})

// VueRouterインスタンスをエクスポートする
// app.jsでインポートするため
export default router
