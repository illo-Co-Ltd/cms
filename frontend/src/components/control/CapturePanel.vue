<template>
    <section>
        
        <div id = "CaptureArea">
            <div class="displayControlTogleBtnArea">
                <h3 class = "btnText">사진 저장</h3>
                <img src="@/assets/icon/icon_home.png" v-on:click="DisplayTogleEvent('CaptureArea')"> <!-- 토글 버튼 -->
            </div>

            <div class="displayControlTogleMainArea">
            <button  id="captureInputBtn" class="InputBtn" v-on:click="CaptureInsert()">시작</button>
            </div>
        </div>
    </section>
</template>


<script>


import {baseURL} from "@/utils/BasicAxiosURL.ts"
import axios from "axios";

const ai = axios.create({
  baseURL
});

export default {
  // DeviceControl.vue에서 파라미터(props) 받아오는 부분
  props : ['projectName','deviceId'],
  setup(props){
    ai; 

        // 토글 버튼 이벤트
    // param : 토글 하고자 하는 항목의 id
    const DisplayTogleEvent = (togleAreaId)=>{
      // 토글 버튼이 켜져있는지 판단.
      if(document.getElementById(togleAreaId).getElementsByClassName('displayControlTogleMainArea')[0].style.display == 'none')
      {
        // 활성화
        document.getElementById(togleAreaId).getElementsByClassName('displayControlTogleMainArea')[0].style.display ='block';
        document.getElementById(togleAreaId).getElementsByClassName('displayControlTogleBtnArea')[0].firstChild.style.color = '#033E5D';
      }
      else
      {
        // 비활성화
        document.getElementById(togleAreaId).getElementsByClassName('displayControlTogleMainArea')[0].style.display='none';
        document.getElementById(togleAreaId).getElementsByClassName('displayControlTogleBtnArea')[0].firstChild.style.color = '#AAA';
      }
    };

    // 캡처 메소드
    const CaptureInsert = () =>{
       ai.post("/control/capture", {
        serial : props.deviceId,
        project : props.projectName,
        x : document.getElementById("absoluteCoordinatesX").value,
        y : document.getElementById("absoluteCoordinatesY").value,
        z : document.getElementById("absoluteCoordinatesZ").value
      }).then(res => {
          console.log(res);
      })
    };

    return {
      props,                      // 시리얼, 프로젝트 명이 들어있는 파라미터
      CaptureInsert,              // 캡처 메소드
      DisplayTogleEvent           // 토글 이벤트
    }
  }
}

</script>

<style lang="scss" scoped>
  @import "@/styles/control.scss";
</style>