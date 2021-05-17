<template lang="html">
  <div>
    <section id="projectMain">
      <ProjectList :arrProjectDevice="state.arrProjectDevice" :arrDevice="state.arrDevice"></ProjectList>
      <DeviceList :arrProjectDevice="state.arrProjectDevice" :arrDevice="state.arrDevice"></DeviceList>
      <DeviceList></DeviceList>
    </section>
  </div>
</template>

<script>

import ProjectList from "@/components/device/ProjectList.vue"
import DeviceList from "@/components/device/DeviceList.vue"
import {useRoute} from 'vue-router'
import {onMounted, reactive} from 'vue'
import axios from "axios";
import {baseURL} from "@/utils/BasicAxiosURL.ts"

const ai = axios.create({
  baseURL
});

export default {
  components : {
    ProjectList,
    DeviceList
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
      projectDeviceInquiry();
      console.log(projectName);
    })

    const deviceInquiry = () => {
      ai.get('/data/device').then(res =>{
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

    const projectDeviceInquiry = () => {
      ai.get('/data/device_entry?project='+projectName).then(res =>{
        for(let i = 0 ; i < res.data.data.length ; i++){
          let projectDeviceData = {};

          projectDeviceData.device = res.data.data[i].serial;
          projectDeviceData.project = res.data.data[i].project;

          state.arrProjectDevice.push(projectDeviceData);
        }
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
    width: 800px;
    min-height: 600px;
    overflow: hidden;
    > * {
      width: 400px;
      float: left;
    }
  }
</style>
