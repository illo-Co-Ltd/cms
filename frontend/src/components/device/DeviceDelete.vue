<template>
  <section>
    <div id="deviceUpdateArea">
      <h1>장비 리스트({{state.deviceCount}})</h1>

      <div id="deviceScroll">

        <div id="deviceListArea" v-for="(array, i) in state.arrDevice" v-bind:key="`B-${i}`">
          <div id="areaLeft">
            <h6>이름 : {{array.serial}}({{array.model}})</h6>
            <h6>담당 : {{array.owner}} : {{array.company}}</h6>
            <h6>IP : {{array.ip}}</h6>
          </div>
          <div id="areaRight" v-on:click="deviceDelete(array)">
            <img src="@/assets/icon/icon_sunny.png"/>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script>

import {reactive, onMounted} from 'vue'
import {baseURL} from "@/utils/BasicAxiosURL.ts"
import axios from "axios";

const ai = axios.create({
  baseURL
});


export default {

  setup(){
    const state = reactive({
      arrDevice : new Array(),
      deviceCount : 0
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

    const deviceDelete = (array) =>{
      ai.delete('/data/device?serial='+array.serial).then(res =>{
        if(res.status === 200){
          console.log('성공');
          state.arrDevice = new Array();
          deviceInquiry();
        }else{
          console.log(res.status + ' : error');
        }
      })
    }

    return {
      state,
      deviceDelete
    }
  }
}
</script>

<style lang="scss" scoped>

@import "@/styles/_mixins.scss";
@import "@/styles/_variables.scss";

  #deviceUpdateArea{
    overflow: hidden;
    width: 100%;
    max-width: 500px;
    margin: 50px auto;

  }

  h1{
    font-size: 30px;
    font-weight: bold;
    margin: 30px 0px;
    text-align: center;
  }

  #deviceScroll{
    height: 400px;
    overflow-y:scroll;
    border: 1px solid #999;
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
    overflow: hidden;
    margin: 0 10px;
    border-bottom: 1px solid #ccc;
    >*{
      float: left;
      font-size: 18px;
      padding: 4px;
      height: 60px;
    }
    >#areaLeft{
      width: 85%;
      line-height: 21px;
      font-size: 15px;
    }
    >#areaRight{
      width: 10%;
      float: right;
      >img{
        width: 25px;
        margin-top: 19px;
        margin-left: 5px;
        background: #999;
      }
    }
  }

</style>
