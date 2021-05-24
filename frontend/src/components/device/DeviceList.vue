<template>
  <section>
    <div id="deviceUpdateArea">
      <h1>추가 가능한 장비({{props.count}})</h1>

      <div id="deviceScroll">

        <div id="deviceListArea" v-for="(array, i) in props.arrDevice" v-bind:key="`B-${i}`">
          <div id="areaLeft">
            <h6>{{array.serial}}({{array.model}})</h6>
            <h6>담당 : {{array.owner}} - {{array.company}}</h6>
            <h6>IP : {{array.ip}}</h6>
          </div>
          <div id="areaRight" v-on:click="projectDeviceInsert(array)">
            <img src="@/assets/icon/icon_sunny.png"/>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script>

import {reactive, inject} from 'vue'
import {baseURL} from "@/utils/BasicAxiosURL.ts"
import axios from "axios";
import {useRoute} from 'vue-router'
const ai = axios.create({
  baseURL
});


export default {
  props : ['arrProjectDevice','arrDevice','count'],
  setup(props){
    const emitter = inject("emitter");
    const state = reactive({
      arrDevice : props.arrDevice,
      arrProjectDevice : props.arrProjectDevice
    });

    const {
      params : {projectName}
    } = useRoute();

    const projectDeviceInsert = (array) =>{
      ai.post('/data/device_entry',{
        serial : array.serial,
        project : projectName
      }).then(res =>{
        if(res.status ===201){

          for(let i = 0 ; i < props.count ; i++){
            if(state.arrDevice[i].serial == array.serial){
              state.arrDevice.splice(i, 1);

              let projectDeviceData = {};
              projectDeviceData.model = array.model;
              projectDeviceData.serial = array.serial;
              projectDeviceData.company = array.company;
              projectDeviceData.owner = array.owner;
              projectDeviceData.ip = array.ip;

              state.arrProjectDevice.push(projectDeviceData);

            }
          }
          emitter.emit('header_Update');
        }
      })
    }

    return {
      state,
      projectDeviceInsert,
      props
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
    margin: 0px auto;

  }

  h1{
    font-size: 23px;
    font-weight: bold;
    text-align: left;
    margin: 30px 0px 10px 30px;
  }

  #deviceScroll{
    height: 400px;
    overflow-y:auto;
    border: 1px solid #999;
    margin: 0 10px;
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
    overflow: hidden;
    margin: 0 10px;
    border-bottom: 1px solid #ccc;
    >*{
      float: left;
      padding: 4px;
      height: 60px;
    }
    >#areaLeft{
      width: calc(100% - 41px);
      line-height: 21px;
      font-size: 14px;
    }
    >#areaRight{
      width: 25px;
      float: right;
      >img{
        width: 25px;
        margin-top: 19px;
        background: #999;
      }
    }
  }

</style>
