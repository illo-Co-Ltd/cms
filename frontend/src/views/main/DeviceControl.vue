<template lang="html">
  <section>
    <div id="introMainArea">

      <div id="titleArea">
        <h6 class="pageTitle">deviceControl</h6>
        <div class="pointLine"></div>
        <h1>{{projectName}} : {{deviceId}} : {{deviceModel}}</h1>
      </div>
    </div>
    <div id="MainArea">
      <div id = "liveCam" >aaa</div>
      <DeviceControlPanel id="deviceControlPanel" ></DeviceControlPanel>
    </div>

  </section>
</template>

<script>

import router from "@/routes/routes.js"
import {useRoute} from 'vue-router'
import {onMounted} from 'vue'
import {baseURL} from "@/utils/BasicAxiosURL.ts"
import axios from "axios";
import DeviceControlPanel from "@/components/control/DeviceControlPanel.vue"

const storage = window.sessionStorage;

const ai = axios.create({
  baseURL
});


export default {
  router,
  components : {
    DeviceControlPanel
  },
  setup(){
    ai;
    storage;
    const {
      params : {projectName},
      params : {deviceId},
      params : {deviceModel}
    } = useRoute()



    onMounted(()=>{
      alert(projectName+' : '+deviceId+' : '+deviceModel);



/*    //sample
      ai.post("/data/user", {
        userid : adminID.value,
        password : adminPass.value,
        username : adminName.value,
        company : adminBelong.value
      },
      {
        headers: {
          "Authorization": 'Bearer '+storage.getItem("access_token")
        }
      }
      ).then(res => {

      }).catch((e) =>{

      })
*/

    })

    return{
      projectName,
      deviceId,
      deviceModel
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
      .pointLine{
        @include length(80px, 5px);
        background: #000;
        margin: 0 auto;
        margin-bottom: 10px;
      }
      .pageTitle{
        font-size: 19px;
        margin: 0 auto;
        padding-top: 20px;
        padding-bottom: 5px;
        text-align: center;
      }
    }

    #MainArea{
      width: calc(100%);
      min-height : 500px;
      margin-bottom: 20px;
    }
    
    #liveCam{
      width: calc(100% - 250px);
      min-height : 500px;
      margin-bottom: 20px;
      display:inline-block;
    }

    #deviceControlPanel{
      min-width : 250px;
      height : 100%;
      display:inline-block;
    }


</style>
