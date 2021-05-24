<template>
    <section>
      <img id = "liveImage" :src="state.src"/>
    </section>
</template>

<script>


import {baseURL} from "@/utils/BasicAxiosURL.ts"
import axios from "axios";
import {onMounted, reactive, onUnmounted} from 'vue';
import Swal from 'sweetalert2/dist/sweetalert2.js';

const ai = axios.create({
  baseURL
});

var timerLiveImage; // 타이머
var isPauseTimer;   // 타이머 실행 확인


export default {
  // DeviceControl.vue에서 파라미터(props) 받아오는 부분
  props : ['projectName','deviceId'],
  setup(props){
    ai;

    // 해당 변수에 변화가 생길 시 값 대입
    const state = reactive({
      src : '/server/control/jpeg/' + props.deviceId,
      srcCount : 1
    });

    // 장치 연결 확인 후 연결되었다면 타이머 실행
    const statusCeck = () =>{
      ai.get('/control/jpeg/'+props.deviceId).then(res =>{
        console.log(res.status);   
        isPauseTimer = true;
        timerLiveImage = setInterval(() => LiveImageRefresh() , 200);
      }).catch((e) =>{
          Swal.fire({
            toast: true,
            position: 'top',
            icon: 'error',
            title: '장치 연결 실패',
            showConfirmButton: false,
            timer: 10000
          })
        console.log("err : ",e);
      });
    }

    onMounted(()=>{
      // 장치 연결 확인
      statusCeck();
    })

    onUnmounted(()=>{
      clearInterval(timerLiveImage);
      isPauseTimer = false;
    })

    const LiveImageRefresh = () => {
      if(isPauseTimer == true)
      {
        state.srcCount = state.srcCount+1;
        state.src = '/server/control/jpeg/'+ props.deviceId+ '?srcCount='+state.srcCount;
      }
    }

    return {
      props,                     // 시리얼, 프로젝트 명이 들어있는 파라미터
      state,
      statusCeck,
      LiveImageRefresh
    }
  }
}


</script>

<style lang="scss" scoped>

  #liveImage{
    width: 100%;
    height: 100%;
  }

</style>