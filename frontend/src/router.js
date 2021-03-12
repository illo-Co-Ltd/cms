import Vue from 'vue'
import Router from 'vue-router'
import MyAuthLayout from '@/layout/MyAuthLayout'
import DashBoardLayout from '@/layout/DashBoardLayout'
import ManageLayout from '@/layout/ManageLayout'

Vue.use(Router)

const router = new Router({
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
          beforeEnter: function(to, from, next) {
            if(sessionStorage.getItem("access_token") != null)
              return next();
            next('/login')
          }
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
          component: () => import('./views/Login.vue'),
          beforeEnter: function(to, from, next) {
            if(sessionStorage.getItem("access_token") != null)
              return next('/dashboard')
            next()              
          }
        },
        {
          path: '/register',
          name: 'register',
          component: () => import('./views/Register.vue')
        },
      ],
    },
    {
      path: '/',
      redirect: 'manage',
      component: ManageLayout,
      children: [
        {
          path: '/manage',
          name: 'manage',
          component: () => import('./views/Manage.vue')
        }
      ]
    }
  ]
})

// router.beforeEach((to, from, next) => {
//   if(sessionStorage.getItem("access_token") != null) {
//     console.log("11")
//     return next();
//   }

//   console.log("22")
//   return next('/login')
// })

export default router