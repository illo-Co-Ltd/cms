


import {createWebHistory, createRouter} from 'vue-router'
import Swal from 'sweetalert2/dist/sweetalert2.js'
import {baseURL} from "@/utils/BasicAxiosURL.ts"
import axios from "axios"


import MainPage from "@/views/main/MainPage.vue"

import Auth from "@/views/login/Auth.vue"
import UserInsert from "@/views/login/UserInsert.vue"

import DashBoard from "@/views/main/DashBoard.vue"
import DeviceControl from "@/views/main/DeviceControl.vue"

import ProjectInsert from "@/views/project/ProjectInsert.vue"
import ProjectUpdate from "@/components/projects/ProjectUpdate.vue"

import DeviceManagement from "@/views/device/DeviceManagement.vue"

import ProjectManagement from "@/views/project/ProjectManagement.vue"


const ai = axios.create({
  baseURL
});

const authCheck = (to, from, next) => {
  to;from;

  ai.get('/auth/whoami').then(res => {
    res;
    next();
  }).catch(e => {
    e;
    Swal.fire({
        toast: true,
        position: 'top',
        icon: 'error',
        title: '로그인이 필요합니다.',
        showConfirmButton: false,
        timer: 3000
       })
    next({ //로그인 페이지로 이동
      path: "/auth",
      query: { redirect: to.fullPath },
    })
  })
}


var routes = [
  {
    path : '/',
    redirect : '/auth'
  },
  {
    path : '/auth',
    component : Auth
  },
  {
    path : '/userInsert',
    component : UserInsert
  },
  {
    path : '/mainPage',
    component : MainPage,
    beforeEnter : authCheck,
    children : [
      {
        path : 'dashBoard',
        component : DashBoard
      },
      {
        path : 'projectInsert',
        component : ProjectInsert
      },
      {
        path : 'deviceControl/:projectName/:deviceId',
        component : DeviceControl
      },
      {
        path : 'deviceManagement',
        component : DeviceManagement
      },
      {
        path : 'projectManagement/:projectName',
        component : ProjectManagement
      },
      {
        path : 'projectUpdate',
        component : ProjectUpdate,
        props : true,
        name : 'projectUpdate'
      }
    ]
  }
];


const history = createWebHistory();


const router = createRouter({
  history,
  routes
});

export default router;
