<template lang="html">
  <section>
    <div id="introMainArea">
      <div id="titleArea">
        <h6 class="pageTitle">deviceControl</h6>
        <div class="pointLine"></div>
        <h1>{{projectName}} : {{deviceId}}}</h1>
      </div>
    </div>
    <div id="MainArea">
      <div id = "liveCam" >
        <LiveImage id="liveImagePanel" :projectName="projectName" :deviceId="deviceId" ></LiveImage>      
      </div>
      <DeviceControlPanel id="deviceControlPanel" :projectName="projectName" :deviceId="deviceId" ></DeviceControlPanel>
    </div>

  </section>
</template>

<script>

import router from "@/routes/routes.js";
import {useRoute} from 'vue-router';
import {baseURL} from "@/utils/BasicAxiosURL.ts";
import axios from "axios";
import DeviceControlPanel from "@/components/control/DeviceControlPanel.vue";
import LiveImage from "@/components/control/LiveImage.vue";

const storage = window.sessionStorage;

const ai = axios.create({
  baseURL
});


export default {
  router,
  components : {
    DeviceControlPanel,
    LiveImage
  },
  setup(){
    ai;
    storage;
    const {
      params : {projectName},
      params : {deviceId},
      params : {deviceModel}
    } = useRoute()

    return{
      projectName,
      deviceId,
      deviceModel,
      LiveImage
    }

  }
}


</script>
<style lang="scss" scoped>

  @import "@/styles/_mixins.scss";
  @import "@/styles/_variables.scss";



    #introMainArea{
      width: calc(100%);
      min-height : 100px;
      margin-bottom: 20px;
    }

    #titleArea{
      min-width: 350px;
      
      .pageTitle{
        font-size: 19px;
        margin: 0 auto;
        padding-top: 20px;
        padding-bottom: 5px;
        text-align: center;
      }
    }

    #MainArea{
      width: calc(100% - 1px);
      min-height : 500px;
      margin-bottom: 20px;
      float: none;
      
      #liveCam{
        width: calc(100% - 250px);
        margin-bottom: 20px;
        height: 100vh; // 화면의 100%

        background-color: aqua;
        display:inline-block;
      }

      #deviceControlPanel{
        min-width : 250px;
        height : 100%;

        background-color:cornsilk;
        display:inline-block;
        float: right;
      }
      
    }
    


</style>
