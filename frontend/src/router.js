import Vue from 'vue'
import Router from 'vue-router'
import MyAuthLayout from '@/layout/MyAuthLayout'
import DashBoardLayout from '@/layout/DashBoardLayout'
Vue.use(Router)

export default new Router({
  linkExactActiveClass: 'active',
  routes: [
    {
      path: '/',
      redirect: 'dashboard',
      component: DashBoardLayout,
      children: [
        {
          path: '/dashboard',
          name: 'dashboard',
          
        },
      ],
    },
    {
      path: '/',
      redirect: 'login',
      component: MyAuthLayout,
      children: [
        {
          path: '/login',
          name: 'login',
          component: () => import('./views/Login.vue')
        },
        {
          path: '/register',
          name: 'register',
          component: () => import('./views/Register.vue')
        },
      ],
    },
  ]
})
