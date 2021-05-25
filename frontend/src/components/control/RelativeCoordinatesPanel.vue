<template>
    <section>
      <div id = "relativeCoordinatesArea">
        <div class="displayControlTogleBtnArea">
            <h3 class = "btnText">상대 좌표 이동</h3>
            <img src="@/assets/icon/icon_home.png" v-on:click="DisplayTogleEvent('relativeCoordinatesArea')"> <!-- 토글 버튼 -->
        </div>
        <div class="displayControlTogleMainArea">
          <div class="inputArea">
              <img src="@/assets/icon/icon_home.png">
              <input type="text" v-model="relativeCoordinatesX"  id="relativeCoordinatesX" placeholder="x" maxlength="6" >
          </div>
              <div class="inputArea">
              <img src="@/assets/icon/icon_home.png">
              <input type="text" v-model="relativeCoordinatesY" id="relativeCoordinatesY" placeholder="y" maxlength="6">
          </div>
              <div class="inputArea">
              <img src="@/assets/icon/icon_home.png">
              <input type="text" v-model="relativeCoordinatesZ" id="relativeCoordinatesZ" placeholder="z" maxlength="6">
          </div>
          <button  id="relativeCoordinatesInputBtn" class="InputBtn" v-on:click="RelativeCoordinatesInsert()">시작</button>
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

    // 상대 좌표 이동 메소드
    const RelativeCoordinatesInsert = () =>{
      // 미구현 
      
       ai.put("/control/pos", {
        serial : props.deviceId,
        x : document.getElementById("relativeCoordinatesX").value,
        y : document.getElementById("relativeCoordinatesY").value,
        z : document.getElementById("relativeCoordinatesZ").value
      }).then(res => {
          console.log(res);
      })
      

    };

    return {
      props,                      // 시리얼, 프로젝트 명이 들어있는 파라미터
      RelativeCoordinatesInsert,  // 상대 좌표 이동 메소드
      DisplayTogleEvent           // 토글 이벤트
    }
  }
}

</script>
<style lang="scss" scoped>
  @import "@/styles/control.scss";
</style>