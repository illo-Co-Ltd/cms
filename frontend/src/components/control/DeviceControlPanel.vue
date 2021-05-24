<template>
    <section>
        <!-- 디스플레이 컨트롤 영역 시작-->
        <div class="togleArea" >
            <!-- 상대 좌표 제어 영역 시작 -->
              <RelativeCoordinatesPanel id="relativeCoordinatesPanel" :projectName="projectName" :deviceId="deviceId" ></RelativeCoordinatesPanel>  
            <!-- 상대 좌표 제어 영역 끝 -->

            <!-- 절대 좌표 제어 영역 시작 -->
              <AbsoluteCoordinatesPanel id="absoluteCoordinatesPanel" :projectName="projectName" :deviceId="deviceId" ></AbsoluteCoordinatesPanel>  
            <!-- 절대 좌표 제어 영역 끝 -->

            <!-- 포커스 제어 영역 시작 -->
              <FocusPanel id="focusPanel" :projectName="projectName" :deviceId="deviceId" ></FocusPanel> 
            <!-- 포커스 제어 영역 끝 -->

            <!-- LED 제어 영역 시작 -->
              <LedPanel id="ledPanel" :projectName="projectName" :deviceId="deviceId" ></LedPanel> 
            <!-- LED 제어 영역 끝 -->

        </div>
    </section>
</template>


<script>


import {baseURL} from "@/utils/BasicAxiosURL.ts"
import axios from "axios";
import AbsoluteCoordinatesPanel from "@/components/control/AbsoluteCoordinatesPanel.vue";
import RelativeCoordinatesPanel from "@/components/control/RelativeCoordinatesPanel.vue";
import FocusPanel from "@/components/control/FocusPanel.vue";
import LedPanel from "@/components/control/LedPanel.vue";

const ai = axios.create({
  baseURL
});

export default {
  // DeviceControl.vue에서 파라미터(props) 받아오는 부분
  props : ['projectName','deviceId'],  
  components : {
    AbsoluteCoordinatesPanel,
    RelativeCoordinatesPanel,
    FocusPanel,
    LedPanel
    
  },
  setup(props){
    ai; 

    return {
      props,                     // 시리얼, 프로젝트 명이 들어있는 파라미터
      RelativeCoordinatesPanel,  // 상대 좌표 이동 컴포넌트
      AbsoluteCoordinatesPanel,  // 절대 좌표 이동 컴포넌트
      FocusPanel,                // 포커스 제어 컴포넌트
      LedPanel                   // LED 제어 컴포넌트
    }
  }
}


</script>
<style lang="scss" scoped>
  @import "@/styles/control.scss";
</style>