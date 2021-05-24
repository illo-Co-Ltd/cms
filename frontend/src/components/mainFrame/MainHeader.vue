<template lang="html">
  <div>
    <div id="mainHeaderArea">
      <img src="@/assets/icon/icon_menu.png" v-on:click="menuEvent()">
      <img src="@/assets/icon/icon_x.png" @click="moveHome()">
      <div>
        <img id="weatherImg" src="@/assets/icon/icon_sunny.png">
        <p><span>현재 15℃</span></p>
      </div>
    </div>
    <div id="mainAsideArea" class="box">

      <div id="asideLoginInfo">
        <div id="loginInfoLeft">
          <img src="@/assets/icon/icon_home.png">
        </div>
        <div id="loginInfoRight">
          <div id="firstLine">
            <h5>{{state.cms_username}}</h5>
            <img @click="logout()" src="@/assets/icon/icon_home.png">
          </div>
          <div class="pointLine"></div>
          <h5>{{state.cms_username}}</h5>
          <h5>{{state.cms_company}}</h5>
        </div>
      </div>

      <div id="asideTitle">
        <button v-on:click="moveProjectInsert()">프로젝트 추가</button>
      </div>
      <ul>

        <div class="menuBigTitle" v-for="(array, i) in state.arrProject" v-bind:key="`B-${i}`">
          <img src="@/assets/icon/icon_home.png">
          <li @click="moveProjectManagement(array)">{{array.name}}({{array.arrDevice.length}})</li>
          <span @click="moveProjectManagement(array)">+</span>
          <div class="menuSmallTitle">
            <h5 v-for="(item, j) in array.arrDevice" v-bind:key="`BB-${j}`" @click="moveDeviceControl(item)">· {{item.serial}}</h5>
          </div>
        </div>

      </ul>
    </div>


    <div id="mobileMainAsideArea" class="box" v-bind:style="{'-webkit-transform' : state.menuAnimation, 'transform' : state.menuAnimation}">

        <div id="asideHeader">
          <img src="@/assets/icon/icon_x.png" v-on:click="menuEvent()">
        </div>

        <div id="asideLoginInfo">
          <div id="loginInfoLeft">
            <img src="@/assets/icon/icon_home.png">
          </div>
          <div id="loginInfoRight">
            <div id="firstLine">
              <h5>{{state.cms_username}}</h5>
              <img @click="logout()" src="@/assets/icon/icon_home.png">
            </div>
            <div class="pointLine"></div>
            <h5>{{state.cms_username}}</h5>
            <h5>{{state.cms_company}}</h5>
          </div>
        </div>



        <div id="asideTitle">
          <button v-on:click="moveProjectInsert()">프로젝트 추가</button>
        </div>

        <ul>

          <div class="menuBigTitle" v-for="(array, i) in state.arrProject" v-bind:key="`B-${i}`">
            <img src="@/assets/icon/icon_home.png">
            <li @click="moveProjectManagement(array)">{{array.name}}({{array.arrDevice.length}})</li>
            <span @click="moveProjectManagement(array)">+</span>
            <div class="menuSmallTitle">
              <h5 v-for="(item, j) in array.arrDevice" v-bind:key="`BB-${j}`" @click="moveDeviceControl(item)">· {{item.serial}}</h5>
            </div>
          </div>

        </ul>
    </div>



  </div>

</template>

<script>
import router from "@/routes/routes.js"
import {onMounted, inject} from 'vue'
import {reactive} from 'vue'
import {baseURL} from "@/utils/BasicAxiosURL.ts"
import axios from "axios"
import Swal from 'sweetalert2/dist/sweetalert2.js'

const storage = window.sessionStorage;
const ai = axios.create({
  baseURL
});

export default {

  setup(){
    const emitter = inject("emitter");
    const state = reactive({
        arrProject : new Array(),
        menuAnimation : 'translate(-400px, 0)',
        cms_username : '',
        cms_company : '',
        cms_userid : '',

    });


    const menuEvent = () => {
      if(state.menuAnimation=='translate(-400px, 0)'){
        state.menuAnimation='translate(0, 0)';
      }else{
        state.menuAnimation='translate(-400px, 0)';
      }
    }

    onMounted(()=>{

      state.cms_username = storage.getItem("cms_username");
      state.cms_company = storage.getItem("cms_company");
      state.cms_userid = storage.getItem("cms_userid");
      updateProject();

    })

    emitter.on('header_Update', () => {
      updateProject();
    })


    const updateProject = () => {
      state.arrProject = new Array();
      ai.get('/data/project').then(res =>{

        for(let i = 0; i < res.data.data.length ; i++){
          let projectData = {};
          projectData.id = res.data.data[i].id;
          projectData.name = res.data.data[i].name;
          projectData.shorthand = res.data.data[i].shorthand;
          projectData.description = res.data.data[i].description;
          projectData.arrDevice = new Array();
          if(res.data.data[i].ended == null){
            state.arrProject.push(projectData);
          }

        }

        for(let i = 0; i < state.arrProject.length ; i++){
          ai.get('/data/device_entry?project='+state.arrProject[i].name).then(innerRes =>{
            for(let j = 0 ; j < innerRes.data.data.length ; j++){
              let projectDeviceData = {};

              projectDeviceData.model = innerRes.data.data[j].model;
              projectDeviceData.serial = innerRes.data.data[j].serial;
              projectDeviceData.company = innerRes.data.data[j].company;
              projectDeviceData.owner = innerRes.data.data[j].owner;
              projectDeviceData.ip = innerRes.data.data[j].ip;
              projectDeviceData.project = innerRes.data.data[j].project;

              state.arrProject[i].arrDevice.push(projectDeviceData);

            }
          })
        }


      });



    }


    const moveDeviceControl = (array) => {
      state.menuAnimation='translate(-400px, 0)';
      router.push('/mainPage/deviceControl/'+array.project+'/'+array.serial);
    }

    const moveProjectInsert = () => {
      state.menuAnimation='translate(-400px, 0)';
      router.push('/mainPage/projectInsert');
    }

    const moveProjectManagement = (array) => {
      state.menuAnimation='translate(-400px, 0)';
      router.push('/mainPage/projectManagement/'+array.name)
    }

    const moveHome = () => {
      state.menuAnimation='translate(-400px, 0)';
      router.push('/mainPage/dashboard');
    }

    const logout = () => {
      ai.get("/auth/logout").then(res => {
        if(res.status === 200){
          storage.setItem("access_token", "");
          storage.setItem("cms_username", "");
          storage.setItem("cms_company", "");
          storage.setItem("cms_userid", "");
          router.push('/');
          Swal.fire({
              toast: true,
              position: 'top',
              icon: 'success',
              title: '로그아웃 성공',
              showConfirmButton: false,
              timer: 3000
             })
        }
      })
    }


    return {
      state,
      menuEvent,
      moveProjectInsert,
      moveDeviceControl,
      moveProjectManagement,
      moveHome,
      logout,
    }
  }
}
</script>

<style lang="scss" scoped>

@import "@/styles/_mixins.scss";
@import "@/styles/_variables.scss";
@import "@/styles/mainHeader.scss";


</style>
