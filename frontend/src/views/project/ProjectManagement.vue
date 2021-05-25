<template lang="html">
  <div>
    <section id="projectMain">
      <ProjectInfomation id="projectInfomation"></ProjectInfomation>
      <ProjectInList id="projectDeviceArea" :arrProjectDevice="state.arrProjectDevice" :arrDevice="state.arrDevice" :count="state.arrProjectDevice.length"></ProjectInList>
      <DeviceList id="deviceArea" :arrProjectDevice="state.arrProjectDevice" :arrDevice="state.arrDevice" :count="state.arrDevice.length"></DeviceList>
    </section>
  </div>
</template>

<script>

import ProjectInList from "@/components/device/ProjectInList.vue"
import DeviceList from "@/components/device/DeviceList.vue"
import ProjectInfomation from "@/components/projects/ProjectInfomation.vue"
import {useRoute} from 'vue-router'
import {onMounted, reactive} from 'vue'
import axios from "axios";
import {baseURL} from "@/utils/BasicAxiosURL.ts"

const ai = axios.create({
  baseURL
});

export default {
  components : {
    ProjectInList,
    DeviceList,
    ProjectInfomation
  },
  setup(){
    const {
      params : {projectName}
    } = useRoute();

    const state = reactive({
      arrProjectDevice : new Array(),
      arrDevice : new Array()
    });

    onMounted(()=>{
      deviceInquiry();
      console.log(projectName);
    })



    const deviceInquiry = () => {
      ai.get('/data/device_entry?project='+projectName).then(res =>{
        for(let i = 0 ; i < res.data.data.length ; i++){
          let projectDeviceData = {};

          projectDeviceData.model = res.data.data[i].model;
          projectDeviceData.serial = res.data.data[i].serial;
          projectDeviceData.company = res.data.data[i].company;
          projectDeviceData.owner = res.data.data[i].owner;
          projectDeviceData.ip = res.data.data[i].ip;
          projectDeviceData.project = res.data.data[i].project;

          state.arrProjectDevice.push(projectDeviceData);

        }

        ai.get('/data/device').then(res =>{
          for(let i = 0 ; i < res.data.data.length ; i++){

            let emptyData = true;
            for(let j = 0; j < state.arrProjectDevice.length ; j++){
              if(state.arrProjectDevice[j].serial == res.data.data[i].serial){
                emptyData = false;
              }
            }
            if(emptyData){
              let deviceData = {};
              deviceData.model = res.data.data[i].model;
              deviceData.serial = res.data.data[i].serial;
              deviceData.company = res.data.data[i].company;
              deviceData.owner = res.data.data[i].owner;
              deviceData.ip = res.data.data[i].ip;
              state.arrDevice.push(deviceData);
            }
          }
        })

      })
    }

    return {
      state
    }
  }
}
</script>

<style lang="scss" scoped>

  #projectMain{
    margin: 0 auto;
    width: 100%;
    max-width: 800px;
    min-height: 600px;
    overflow: hidden;
    min-width: 300px;
    margin-bottom: 30px;
    > #projectInfomation{
      width: 100%;
    }

    #projectDeviceArea, #deviceArea {
      width: 50%;
      float: left;
    }
  }

  // 800 이하가 되면 aside 감춤
  @media ( max-width: 600px ) {
    #projectMain{
      > #projectDeviceArea, #deviceArea {
        width: 100%;
      }
    }
  }


</style>
