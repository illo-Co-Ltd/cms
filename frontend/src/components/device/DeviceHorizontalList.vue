<template>
  <section>
    <div id="deviceUpdateArea">
      <h1>장비 리스트({{state.arrDevice.length}})</h1>
      <h2 @click="moveDeviceManagement()">장비관리 ></h2>
      <div id="deviceScroll">

        <div id="deviceListArea" v-for="(array, i) in state.arrDevice" v-bind:key="`B-${i}`">
          <img src="@/assets/icon/icon_sunny.png"/>
          <h6>{{array.serial}}</h6>
        </div>

      </div>
    </div>
  </section>
</template>

<script>

import {reactive, onMounted} from 'vue'
import {baseURL} from "@/utils/BasicAxiosURL.ts"
import axios from "axios";
import router from "@/routes/routes.js"

const ai = axios.create({
  baseURL
});


export default {
  setup(){
    const state = reactive({
      arrDevice : new Array(),
    });

    onMounted(()=>{
      deviceInquiry();
    })

    const deviceInquiry = () => {
      ai.get('/data/device').then(res =>{
        state.deviceCount = res.data.data.length;
        for(let i = 0 ; i < res.data.data.length ; i++){
          let deviceData = {};

          deviceData.model = res.data.data[i].model;
          deviceData.serial = res.data.data[i].serial;
          deviceData.company = res.data.data[i].company;
          deviceData.owner = res.data.data[i].owner;
          deviceData.ip = res.data.data[i].ip;

          state.arrDevice.push(deviceData);
        }
      })
    }

    const moveDeviceManagement = () => {
      router.push('/mainPage/deviceManagement/');
    }


    return {
      state,
      moveDeviceManagement
    }
  }
}
</script>

<style lang="scss" scoped>

@import "@/styles/_mixins.scss";
@import "@/styles/_variables.scss";

  #deviceUpdateArea{
    overflow: hidden;
    width: calc( 100% - 20px);
    padding: 0 10px;
    margin: 50px auto;
    margin-top: 0px;

  }

  h1{
    font-size: 25px;
    font-weight: bold;
    margin-left: 15px;
    margin-bottom: 15px;
    text-align: left;
  }
  h2{
    font-size: 13px;
    margin-bottom: 5px;
    text-align: right;
  }
  #deviceScroll{
    height: 120px;
    width: 100%;
    white-space : nowrap;
    overflow-x : scroll;
    overflow-y : hidden;
    border: 1px solid #999;
    @include border-radius(10px);
  }

  #deviceScroll::-webkit-scrollbar {
    width: 10px;
  }
  #deviceScroll::-webkit-scrollbar-thumb {
    background-color: #dbdbdb;
    border-radius: 10px;
    background-clip: padding-box;
    border: 2px solid transparent;
  }
  #deviceScroll::-webkit-scrollbar-track {
    background-color: grey;
    border-radius: 10px;
    box-shadow: inset 0px 0px 5px white;
  }


  #deviceListArea{
    margin: 5px 5px;
    border : 1px solid #ccc;
    display: inline-block;

    background: #00ff0044;

    @include border-radius(10px);

    width: 95px;
    height: 90px;
    >img{
      margin-left: 13px;
      margin-top: 2px;
      width: 68px;
      height: 68px;
    }
    >h6{
      font-size: 14px;
      text-align: center;
    }
  }

</style>
