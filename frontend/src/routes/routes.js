


import {createWebHistory, createRouter} from 'vue-router'

import MainPage from "@/views/main/MainPage.vue"

import Auth from "@/views/login/Auth.vue"
import UserInsert from "@/views/login/UserInsert.vue"

import DashBoard from "@/views/main/DashBoard.vue"
import DeviceControl from "@/views/main/DeviceControl.vue"

import ProjectInsert from "@/views/project/ProjectInsert.vue"

import DeviceManagement from "@/views/device/DeviceManagement.vue"

import ProjectManagement from "@/views/project/ProjectManagement.vue"

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
